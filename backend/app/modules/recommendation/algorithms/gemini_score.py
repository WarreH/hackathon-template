from app.modules.dataset.gemini import Gemini
from app.modules.recommendation.recommendation_py_models import PyCandidateResult, PyRecQuery


def gemini_together(user_query: PyRecQuery,
                 candidates: list[PyCandidateResult]) -> list[float]:
    """
    Inserting user_query and candidate as model_dump into gemini and generating score
    Expecting a float between 0.1 and 1.0

    :param user_query:
    :param candidates:
    :return:
    """

    message = f"""
    I have a user_query object with user preferences, and a list of candidate locations.
    Given a user_query object with user preferences and a list of candidate locations, score each location based on how interesting it is for the user. Use a float between 0.0 (not interesting) and 1.0 (highly interesting). 
    Base the score on: (1) how well the location’s tags match the user’s preferences, and (2) the location’s appeal as a fun tourist activity (e.g., unique experiences, scenic beauty, or exciting activities score higher). 
    Ensure scores vary by comparing tag relevance and tourist appeal, avoiding identical values unless justified.

    Preference Match Score (0.0–0.5): Count the number of user preference tags that match the location’s tags. Divide by the total number of user preference tags to get a fraction, then multiply by 0.5. If no tags match or no preferences are provided, score 0.0.

    Tourist Fun Score (0.0–0.5): Assign a score based on the location’s appeal as a tourist activity using this table:

    Adventure (e.g., ziplining, hiking): 0.5
    Scenic (e.g., beaches, parks): 0.4
    Cultural (e.g., museums, historical sites): 0.2
    Generic (e.g., malls, urban areas): 0.1 Adjust slightly based on tags if relevant (e.g., “nature” boosts scenic appeal).
    Total Score: Add Preference Match Score and Tourist Fun Score, ensuring the result is between 0.0 and 1.0. 
    
    Return only a raw Python list of floats, like [0.2, 0.8, 0.5] — no explanation, no code block, no extra formatting.
    This is the user_query: {user_query.model_dump()}
    These are the candidates locations:
    """
    for i, candidate in enumerate(candidates):
        message += f"Candidate {i}: {candidate.model_dump(include={"osm_tags"})}\n"

    gemini = Gemini()
    result = gemini.prompt(message=message)

    formatted_result = result.text.replace("`", "").replace("python", "")

    try:
        evaluated_result = eval(formatted_result)
    except Exception as e:
        print(f"{formatted_result} gives {e}")
        return [0.1] * len(candidates)

    if not evaluated_result or len(evaluated_result) == 0:
         return [0.1] * len(candidates)

    # Fixing missing values
    evaluated_result += [min(evaluated_result)] * (len(candidates) - len(evaluated_result))
    return evaluated_result
