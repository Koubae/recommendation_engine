
from recommendation_engine.app.recommendation.algorithm import generate_recommendation_subsequences


def main():
    product_ids = (1, 2, 3, 4)
    subsequences = generate_recommendation_subsequences(product_ids)
    print(subsequences)


if __name__ == '__main__':
    main()
