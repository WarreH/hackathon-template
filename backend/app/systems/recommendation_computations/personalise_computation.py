from app.modules.recommendation.recommendation_py_models import PyRecommendedResult, PyCandidateResult


def personalise_computation(candidates: list[PyCandidateResult]) -> list[PyRecommendedResult]:
    """
    From candidate list we apply a more thorough filter to tailer to the user

    :param candidates:
    :return:
    """
    resulting_scores = []

    for candidate in candidates:
        ensemble_scores: dict[str, float] = {"boop": 1.0} # TODO
        score = sum(ensemble_scores.values())

        resulting_scores.append(
            PyRecommendedResult(
                **candidate.model_dump(),
                score=score,
                ensemble_scores=ensemble_scores,
            )
        )
    return resulting_scores
