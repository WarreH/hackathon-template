from app.modules.recommendation.recommendation_py_models import PyRecommendedResult, PyCandidateResult, PyRecQuery
from app.systems.recommendation_computations.candidate_computation import candidate_computation
from app.systems.recommendation_computations.personalise_computation import personalise_computation


async def recommend_locations(user_query_param: PyRecQuery,
                              n_recommendations: int) -> list[PyRecommendedResult]:
    """
    Top recommendation function.
    TO BE CALLED IN ENDPOINT

    :param user_query_param:
    :param n_recommendations: Maximum Requested recommendations (could be less!)
    :return: list of recommended locations
    """

    # -----
    # 1) Generate candidates
    # -----
    candidate_n = n_recommendations+10
    candidates: list[PyCandidateResult] = candidate_computation(user_query_param=user_query_param,
                                             candidate_n=candidate_n)

    # -----
    # 2) Apply ensembles to each item in candidate list
    # -----
    computed_recommendations: list[PyRecommendedResult] = personalise_computation(candidates=candidates)

    # -----
    # 3) Sort by rank and return
    # -----
    sorted_recommendations = sorted(computed_recommendations,
                                    key=lambda recommendation: recommendation.score,
                                    reverse=True)
    return [recommendation for
            recommendation in
            sorted_recommendations[:max(n_recommendations, len(sorted_recommendations))]
            ]