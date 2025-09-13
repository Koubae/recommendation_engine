import hashlib
import json
from itertools import combinations

from recommendation_engine.app.recommendation.types import (
    TProductIdsFingerPrint,
    TProductIdsOrderedAndUnique,
    TRecommendationSubSequences,
)


def generate_recommendation_subsequences(
    product_ids: tuple[int, ...] | list[int],
) -> tuple[TProductIdsOrderedAndUnique, TRecommendationSubSequences]:
    """Generate all non-repeated subsequences of product IDs.

    The input sequence of product IDs is first sorted in ascending order.
    Then, all unique combinations are generated and returned, ordered by
    subsequence length and lexicographically within each length.

    Example:
        >>> generate_recommendation_subsequences([3, 1, 2])
        [
            [1],
            [2],
            [3],
            [1, 2],
            [1, 3],
            [2, 3],
            [1, 2, 3]
        ]
    """
    unique_ordered_product_ids = sorted(set(product_ids))
    count = len(unique_ordered_product_ids)

    subsequences: list[list[int]] = []
    for sequence_length in range(1, count + 1):
        sequences_iter = combinations(unique_ordered_product_ids, sequence_length)
        subsequences.extend([list(sequence) for sequence in sequences_iter])
    return unique_ordered_product_ids, subsequences


def generate_product_ids_fingerprint(product_ids: TProductIdsOrderedAndUnique) -> TProductIdsFingerPrint:
    """Creates a unique hash for a sequence of product IDs.

    The product_ids passed should be sorted and unique.
    """
    product_ids_serialized = json.dumps(product_ids, separators=(",", ":"))
    return hashlib.sha1(product_ids_serialized.encode("utf-8")).hexdigest()
