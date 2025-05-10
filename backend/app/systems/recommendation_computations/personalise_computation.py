from app.modules.recommendation.algorithms.gemini_score import gemini_together
from app.modules.recommendation.algorithms.generate_description import gemini_description, gemini_batch_description
from app.modules.recommendation.algorithms.proximity_score import proximity_score
from app.modules.recommendation.recommendation_py_models import PyRecommendedResult, PyCandidateResult, PyRecQuery
from app.systems.recommendation_computations.label_candidate import label_candidate


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

    print("Labeling")
    for candidate in candidates:
        label = label_candidate(candidate)
        candidate.osm_tags["label"] = label

    # Gemini evaluate together
    print("Scoring together")
    together_scores: list[float] = gemini_together(user_query=user_query, candidates=candidates)
    print(together_scores)
    for i, candidate in enumerate(candidates):
        ensemble_scores[i]["gemini_together"] = together_scores[i]

    proximity_scores = proximity_score(candidates=candidates)
    for i, ensemble, candidate in zip(range(len(candidates)) ,ensemble_scores, candidates):
        ensemble["proximity"] = proximity_scores[i]
        score = sum(ensemble.values())

        resulting_scores.append(
            PyRecommendedResult(
                **candidate.model_dump(),
                score=score,
                ensemble_scores=ensemble,
                description=candidate.osm_tags["description"],
                name=candidate.osm_tags["name"],
                label=candidate.osm_tags["label"],
            )
        )
    return resulting_scores
