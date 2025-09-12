import typing as t
from itertools import combinations


def generate_recommendation_subsequences(product_ids: t.Sequence[int]) -> list[list[int]]:
    count = len(product_ids)

    subsequences: list[list[int]] = []
    for sequence_length in range(1, count + 1):
        sequences_iter = combinations(product_ids, sequence_length)
        subsequences.extend([list(sequence) for sequence in sequences_iter])
    return subsequences
