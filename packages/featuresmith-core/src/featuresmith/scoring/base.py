"""Extension-point interface for one ML Readiness scoring dimension.

A scoring dimension is a pure, deterministic consumer of a ``ReviewResult``:
it reads only the review's sections (never raw data) and produces a single
``DimensionScore``. Dimensions are the stable extension point of the ML
Readiness Score, mirroring how reviewers are the extension point of the Review
Engine. See ``docs/features/ML-Readiness-Score.md`` section 8.1.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from featuresmith.scoring.schema import DimensionScore

if TYPE_CHECKING:
    from featuresmith.review.schema import ReviewResult


class ScoreDimension(Protocol):
    """Interface implemented by every scoring dimension.

    Implementations are stateless and deterministic: the same ``ReviewResult``
    always yields the same ``DimensionScore``. A dimension declares which
    review sections it reads and opts out via ``applicable()`` rather than
    inventing a fixed score for datasets it does not apply to.
    """

    id: str
    label: str
    default_weight: float

    def applicable(self, result: ReviewResult) -> bool:
        """Return whether this dimension applies to the given review.

        Args:
            result: The frozen ReviewResult.

        Returns:
            True when the dimension should contribute to the overall score.
        """
        ...

    def compute(self, result: ReviewResult) -> DimensionScore:
        """Compute this dimension's score and explanation.

        Args:
            result: The frozen ReviewResult.

        Returns:
            The frozen DimensionScore for this dimension.
        """
        ...
