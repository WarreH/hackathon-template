from app.modules.dataset.gemini import Gemini
from app.modules.recommendation.recommendation_py_models import PyCandidateResult


def gemini_description(candidate: PyCandidateResult):
    message = f"""
    Create a joyful and happy description of a location based on provided location information. 
    Write as if you're a tourist visiting the location for the first time, unaware of its details. 
    Keep the description vibrant and engaging, with a maximum of 100 words. 
    This is all the information we have: {candidate.model_dump()}"""

    gemini = Gemini()
    result = gemini.prompt(message=message)

    return result.text

def gemini_batch_description(candidates: list[PyCandidateResult]) -> list[str]:
    message = f"""
    Create a joyful and happy description of a location based on provided location information. 
    Write this for a tourist visiting the location for the first time, unaware of its details.
    This description is written one a board standing next to the location. 
    Keep the description vibrant and engaging, with a maximum of 100 words. 
    
    Make sure you have a description for each candidate. Check yourself to make sure you have a description for each location.
    
    Return only a raw Python list of string, like ["description_one", "description_two", "description_three"] — no explanation, no code block, no extra formatting.
    """
    for i, candidate in enumerate(candidates):
        message += f"Candidate {i}: {candidate.model_dump()}\n"

    gemini = Gemini()
    result = gemini.prompt(message=message)

    formatted_result = result.text.replace("`", "").replace("python", "")

    return eval(formatted_result)
