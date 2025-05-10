from app.modules.recommendation.recommendation_py_models import PyCandidateResult


def proximity_score(candidates: list[PyCandidateResult]) -> list[float]:
    distances =  list(map(lambda c: c.distance, candidates))

    max_distance = max(distances)

    return [
        1 / (c.distance / max_distance) for c in candidates
    ]
