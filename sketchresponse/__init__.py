"""SketchResponse - A tool for drawing and evaluating mathematical functions."""

from .sketchresponse import GradeableCollection, GraderReturn, config, grader
from .types import (
    GraderResult,
    SketchAnswer,
    SketchCanvasSize,
    SketchConfig,
    SketchDrawing,
    SketchGradeableData,
    SketchGrader,
    SketchItem,
    SketchMeta,
    SketchSubmission,
    SketchTool,
)

__all__ = [
    # Runtime API
    "grader",
    "config",
    "GradeableCollection",
    "sketchresponse",
    # Result / return types
    "GraderResult",
    "GraderReturn",
    # Data-shape TypedDicts
    "SketchAnswer",
    "SketchCanvasSize",
    "SketchConfig",
    "SketchDrawing",
    "SketchGradeableData",
    "SketchGrader",
    "SketchItem",
    "SketchMeta",
    "SketchSubmission",
    "SketchTool",
]
