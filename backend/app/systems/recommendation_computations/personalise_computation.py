from app.modules.recommendation.algorithms.gemini_score import gemini_together
from app.modules.recommendation.algorithms.generate_description import gemini_description, gemini_batch_description
from app.modules.recommendation.recommendation_py_models import PyRecommendedResult, PyCandidateResult, PyRecQuery


def personalise_computation(user_query: PyRecQuery, candidates: list[PyCandidateResult]) -> list[PyRecommendedResult]:
    """
    From candidate list we apply a more thorough filter to tailer to the user

    :param user_query:
    :param candidates:
    :return:
    """
    resulting_scores = []

    ensemble_scores: list[dict[str, float]] = [{}] * len(candidates)

    # Generating description
    print("Generating description...")
    try:
        desc_list = gemini_batch_description(candidates)
        print(len(desc_list))
        for desc, candidate in zip(desc_list, candidates):
            candidate.osm_tags["description"] = desc
    except Exception as e:
        print(f"Can't batch descript {e}")
        for candidate in candidates:
            description = gemini_description(candidate)
            candidate.osm_tags["description"] = description

    # Gemini evaluate together
    print("Scoring together")
    together_scores: list[float] = gemini_together(user_query=user_query, candidates=candidates)
    for i, candidate in enumerate(candidates):
        ensemble_scores[i]["gemini_together"] = together_scores[i]

    print("Boop")
    for ensemble, candidate in zip(ensemble_scores, candidates):
        score = sum(ensemble.values())

        resulting_scores.append(
            PyRecommendedResult(
                **candidate.model_dump(),
                score=score,
                ensemble_scores=ensemble,
                description=candidate.osm_tags["description"]
            )
        )
    return resulting_scores
