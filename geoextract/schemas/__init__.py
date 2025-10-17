"""Data schemas for geological document processing."""

from .document import DocumentMetadata, GeologicalDocument
from .geological import (
    Location,
    Sample,
    GeologicalObservation,
    AssayResult,
    Coordinate,
    StructuralMeasurement,
)

__all__ = [
    "DocumentMetadata",
    "GeologicalDocument",
    "Location",
    "Sample", 
    "GeologicalObservation",
    "AssayResult",
    "Coordinate",
    "StructuralMeasurement",
]