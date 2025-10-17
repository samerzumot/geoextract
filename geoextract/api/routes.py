"""API routes for GeoExtract."""

import json
import logging
import shutil
import tempfile
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional
import zipfile

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Form
from pydantic import BaseModel

from geoextract.api import job_store
from geoextract.config import settings
from geoextract.export.csv_writer import CSVWriter
from geoextract.export.geojson_writer import GeoJSONWriter
from geoextract.extraction.entity_extractor import EntityExtractor
from geoextract.ocr.ocr_manager import OCRManager
from geoextract.preprocessing.image_clean import ImageCleaner
from geoextract.preprocessing.pdf_handler import PDFHandler
from geoextract.schemas.document import GeologicalDocument, DocumentMetadata, ProcessingStats

logger = logging.getLogger(__name__)

router = APIRouter()

class ProcessingRequest(BaseModel):
    """Request model for document processing."""
    llm_provider: Optional[str] = "ollama"
    llm_model: Optional[str] = "llama3.1:8b"
    ocr_engine: Optional[str] = "paddle"
    confidence_threshold: Optional[float] = 0.8
    language: Optional[str] = "en"
    output_format: Optional[List[str]] = ["geojson"]
    debug: Optional[bool] = False

class JobStatus(BaseModel):
    """Job status model."""
    job_id: str
    status: str  # pending, processing, completed, failed
    progress: float  # 0.0 to 1.0
    message: str
    result_path: Optional[str] = None
    error: Optional[str] = None

@router.post("/process", response_model=JobStatus)
async def process_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    llm_provider: str = Form("ollama"),
    llm_model: str = Form("llama3.1:8b"),
    ocr_engine: str = Form("paddle"),
    confidence_threshold: float = Form(0.8),
    language: str = Form("en"),
    output_format: str = Form("geojson"),
    debug: bool = Form(False)
):
    """Process a single PDF document."""
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Initialize job status
    job_store.create_job(job_id, {
        "job_id": job_id,
        "status": "pending",
        "progress": 0.0,
        "message": "Job created",
        "result_path": None,
        "error": None
    })
    
    # Start background processing
    temp_pdf_path, cleanup_callback = await _persist_upload(file)

    output_formats = [fmt.strip() for fmt in output_format.split(",") if fmt.strip()]
    if not output_formats:
        raise HTTPException(status_code=400, detail="At least one output format must be specified")

    background_tasks.add_task(
        process_document_background,
        job_id,
        temp_pdf_path,
        cleanup_callback,
        llm_provider,
        llm_model,
        ocr_engine,
        confidence_threshold,
        language,
        output_formats,
        debug
    )
    
    return JobStatus(
        job_id=job_id,
        status="pending",
        progress=0.0,
        message="Job created"
    )

@router.post("/process/batch", response_model=JobStatus)
async def process_batch(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    llm_provider: str = Form("ollama"),
    llm_model: str = Form("llama3.1:8b"),
    ocr_engine: str = Form("paddle"),
    confidence_threshold: float = Form(0.8),
    language: str = Form("en"),
    output_format: str = Form("geojson"),
    debug: bool = Form(False)
):
    """Process multiple PDF documents."""
    
    # Validate files
    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail=f"File {file.filename} must be a PDF")
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Initialize job status
    job_store.create_job(job_id, {
        "job_id": job_id,
        "status": "pending",
        "progress": 0.0,
        "message": "Batch job created",
        "result_path": None,
        "error": None
    })
    
    # Start background processing
    persisted_files: List[Path] = []
    cleanup_callbacks: List[Callable[[], None]] = []
    for file in files:
        temp_path, cleanup_callback = await _persist_upload(file)
        persisted_files.append(temp_path)
        cleanup_callbacks.append(cleanup_callback)

    output_formats = [fmt.strip() for fmt in output_format.split(",") if fmt.strip()]
    if not output_formats:
        raise HTTPException(status_code=400, detail="At least one output format must be specified")

    background_tasks.add_task(
        process_batch_background,
        job_id,
        persisted_files,
        cleanup_callbacks,
        llm_provider,
        llm_model,
        ocr_engine,
        confidence_threshold,
        language,
        output_formats,
        debug
    )
    
    return JobStatus(
        job_id=job_id,
        status="pending",
        progress=0.0,
        message="Batch job created"
    )

def process_document_background(
    job_id: str,
    pdf_path: Path,
    cleanup_callback: Callable[[], None],
    llm_provider: str,
    llm_model: str,
    ocr_engine: str,
    confidence_threshold: float,
    language: str,
    output_formats: List[str],
    debug: bool
):
    """Background task for processing a single document."""

    try:
        job_store.update_job(
            job_id,
            status="processing",
            message="Starting processing",
            progress=0.05
        )

        processor = DocumentProcessor(
            llm_provider=llm_provider,
            llm_model=llm_model,
            ocr_engine=ocr_engine,
            confidence_threshold=confidence_threshold,
            language=language,
            debug=debug,
            progress_callback=lambda progress, message: job_store.update_job(
                job_id,
                progress=progress,
                message=message
            )
        )

        result_zip = processor.process_single(pdf_path, output_formats)

        job_store.update_job(
            job_id,
            status="completed",
            progress=1.0,
            message="Processing completed successfully",
            result_path=str(result_zip)
        )

        logger.info("Job %s completed successfully", job_id)

    except Exception as exc:  # pragma: no cover - runtime safety
        logger.exception("Job %s failed: %s", job_id, exc)
        job_store.update_job(
            job_id,
            status="failed",
            error=str(exc),
            message=f"Processing failed: {exc}"
        )
    finally:
        _safe_cleanup(cleanup_callback)


def process_batch_background(
    job_id: str,
    file_paths: List[Path],
    cleanup_callbacks: List[Callable[[], None]],
    llm_provider: str,
    llm_model: str,
    ocr_engine: str,
    confidence_threshold: float,
    language: str,
    output_formats: List[str],
    debug: bool
):
    """Background task for processing multiple documents."""

    try:
        job_store.update_job(
            job_id,
            status="processing",
            message=f"Processing {len(file_paths)} files",
            progress=0.05
        )

        processor = DocumentProcessor(
            llm_provider=llm_provider,
            llm_model=llm_model,
            ocr_engine=ocr_engine,
            confidence_threshold=confidence_threshold,
            language=language,
            debug=debug,
            progress_callback=lambda progress, message: job_store.update_job(
                job_id,
                progress=progress,
                message=message
            )
        )

        result_zip = processor.process_batch(file_paths, output_formats)

        job_store.update_job(
            job_id,
            status="completed",
            progress=1.0,
            message=f"Batch processing completed: {len(file_paths)} files processed",
            result_path=str(result_zip)
        )

        logger.info("Batch job %s completed successfully", job_id)

    except Exception as exc:  # pragma: no cover - runtime safety
        logger.exception("Batch job %s failed: %s", job_id, exc)
        job_store.update_job(
            job_id,
            status="failed",
            error=str(exc),
            message=f"Batch processing failed: {exc}"
        )
    finally:
        for callback in cleanup_callbacks:
            _safe_cleanup(callback)


async def _persist_upload(upload: UploadFile) -> tuple[Path, Callable[[], None]]:
    """Persist an uploaded file to disk for background processing."""

    uploads_dir = settings.temp_dir / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(upload.filename or "document.pdf").name
    target_path = uploads_dir / f"{uuid.uuid4()}_{safe_name}"

    try:
        with target_path.open("wb") as buffer:
            while True:
                chunk = await upload.read(1024 * 1024)
                if not chunk:
                    break
                buffer.write(chunk)
    finally:
        await upload.close()

    def cleanup() -> None:
        if target_path.exists():
            try:
                target_path.unlink()
            except Exception as cleanup_error:  # pragma: no cover - best effort clean
                logger.warning("Failed to remove temporary upload %s: %s", target_path, cleanup_error)

    return target_path, cleanup


def _safe_cleanup(callback: Optional[Callable[[], None]]) -> None:
    """Invoke cleanup callback, ignoring errors."""

    if callback is None:
        return

    try:
        callback()
    except Exception as cleanup_error:  # pragma: no cover - best effort clean
        logger.warning("Cleanup callback failed: %s", cleanup_error)

@router.get("/jobs")
async def list_jobs():
    """List all jobs."""
    return {"jobs": job_store.list_jobs()}

@router.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    """Delete a job and its results."""
    job = job_store.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Delete result file if it exists
    if job.get("result_path"):
        result_path = Path(job["result_path"])
        if result_path.exists():
            result_path.unlink()
    
    # Remove job from storage
    job_store.delete_job(job_id)
    
    return {"message": "Job deleted successfully"}

@router.get("/config")
async def get_config():
    """Get current configuration."""
    return {
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model,
        "ocr_engine": settings.ocr_engine,
        "ocr_language": settings.ocr_language,
        "ocr_confidence_threshold": settings.ocr_confidence_threshold,
        "pdf_dpi": settings.pdf_dpi,
        "max_file_size_mb": settings.max_file_size_mb,
        "output_dir": str(settings.output_dir),
        "debug": settings.debug
    }