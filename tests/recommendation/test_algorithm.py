import pytest

from recommendation_engine.app.recommendation.algorithm import (
    generate_product_ids_fingerprint,
    generate_recommendation_subsequences,
)
from tests.data.recommendation_sequences_samples import RECOMMENDATIONS_SEQUENCES_SAMPLES


@pytest.mark.unit
class TestUnitRecommendationAlgorithms:
    @pytest.mark.parametrize("input_ids, expected", RECOMMENDATIONS_SEQUENCES_SAMPLES)
    def test_generate_recommendation_subsequences(self, input_ids: tuple[int, ...], expected: list[list[int]]):
        _, recommendations = generate_recommendation_subsequences(input_ids)
        assert recommendations == expected

    def test_generate_recommendation_subsequences_realistic_case(self):
        product_ids = (1234, 13034, 30324, 33912, 240234)

        _, recommendations = generate_recommendation_subsequences(product_ids)
        expected = [
            [1234],
            [13034],
            [30324],
            [33912],
            [240234],
            [1234, 13034],
            [1234, 30324],
            [1234, 33912],
            [1234, 240234],
            [13034, 30324],
            [13034, 33912],
            [13034, 240234],
            [30324, 33912],
            [30324, 240234],
            [33912, 240234],
            [1234, 13034, 30324],
            [1234, 13034, 33912],
            [1234, 13034, 240234],
            [1234, 30324, 33912],
            [1234, 30324, 240234],
            [1234, 33912, 240234],
            [13034, 30324, 33912],
            [13034, 30324, 240234],
            [13034, 33912, 240234],
            [30324, 33912, 240234],
            [1234, 13034, 30324, 33912],
            [1234, 13034, 30324, 240234],
            [1234, 13034, 33912, 240234],
            [1234, 30324, 33912, 240234],
            [13034, 30324, 33912, 240234],
            [1234, 13034, 30324, 33912, 240234],
        ]
        assert recommendations == expected

    def test_generate_recommendation_subsequences_unsorted(self):
        """GIVEN a list of product ids; WHEN the list is unsorted,
        THEN the algorithm should generated sorted output"""
        product_ids = (3, 2, 1)
        unique_ordered_product_ids, recommendations = generate_recommendation_subsequences(product_ids)
        expected = [[1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
        assert recommendations == expected
        assert unique_ordered_product_ids == [1, 2, 3]

    def test_generate_recommendation_subsequences_unique_values(self):
        """GIVEN a list of product ids; WHEN the list contains repeated values,
        THEN the algorithm should generated sorted output"""
        product_ids = (1, 2, 3, 1, 2, 3)
        unique_ordered_product_ids, recommendations = generate_recommendation_subsequences(product_ids)
        expected = [[1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
        assert recommendations == expected
        assert unique_ordered_product_ids == [1, 2, 3]

    def test_generate_recommendation_subsequences_empty(self):
        unique_ordered_product_ids, recommendations = generate_recommendation_subsequences([])

        assert unique_ordered_product_ids == []
        assert recommendations == []

    def test_generate_product_ids_fingerprint(self):
        product_ids = [1, 2, 3]
        fingerprint = generate_product_ids_fingerprint(product_ids)

        assert fingerprint == "9ef50cc82ae474279fb8e82896142702bccbb33a"
