from itertools import combinations

from recommendation_engine.app.recommendation.types import TRecommendationSubSequences


def generate_recommendation_subsequences(product_ids: tuple[int, ...] | list[int]) -> TRecommendationSubSequences:
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
    product_ids = sorted(product_ids)
    count = len(product_ids)

    subsequences: list[list[int]] = []
    for sequence_length in range(1, count + 1):
        sequences_iter = combinations(product_ids, sequence_length)
        subsequences.extend([list(sequence) for sequence in sequences_iter])
    return subsequences
