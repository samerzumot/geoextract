"""OCR engines for text extraction from images."""

from .paddle_engine import PaddleOCREngine
from .tesseract_engine import TesseractEngine
from ocr.ocr_manager import OCRManager

__all__ = ["PaddleOCREngine", "TesseractEngine", "OCRManager"]