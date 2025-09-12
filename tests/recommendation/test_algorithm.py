import pytest

from recommendation_engine.app.recommendation.algorithm import generate_recommendation_subsequences
from tests.data.recommendation_sequences_samples import RECOMMENDATIONS_SEQUENCES_SAMPLES


@pytest.mark.unit
class TestRecommendationAlgorithms:

    @pytest.mark.parametrize("input_ids, expected", RECOMMENDATIONS_SEQUENCES_SAMPLES)
    def test_generate_recommendation_subsequences(self, input_ids: tuple[int, ...], expected: list[list[int]]):
        recommendations = generate_recommendation_subsequences(input_ids)
        assert expected == recommendations
