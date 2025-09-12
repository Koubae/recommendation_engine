import pytest

from recommendation_engine.app.recommendation.algorithm import generate_recommendation_subsequences
from tests.data.recommendation_sequences_samples import RECOMMENDATIONS_SEQUENCES_SAMPLES


@pytest.mark.unit
class TestRecommendationAlgorithms:

    @pytest.mark.parametrize("input_ids, expected", RECOMMENDATIONS_SEQUENCES_SAMPLES)
    def test_generate_recommendation_subsequences(self, input_ids: tuple[int, ...], expected: list[list[int]]):
        recommendations = generate_recommendation_subsequences(input_ids)
        assert expected == recommendations

    def test_generate_recommendation_subsequences_realistic_case(self):
        product_ids = sorted((1234, 33912, 30324, 13034, 240234))

        recommendations = generate_recommendation_subsequences(product_ids)
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
            [1234, 13034, 30324, 33912, 240234]
        ]
        assert expected == recommendations
