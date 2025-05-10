from app.modules.dataset.gemini import Gemini


def label_candidate(candidate):
    categories = [
        "Food & Drink",
        "Cultural"
        "Shops",
        "Leisure",
        "Sports",
        "Public Transit",
        "Heritage Monuments",
        "Residential",
        "Health & Emergency",
        "Entertainement"
    ]

    gemini = Gemini()
    resp = gemini.prompt(
        "Given this list of categories. Look at the value of the data and choose in which categorie it"
        "needs to be! So as response give the name of the categorie that fits the value the best. So"
        "for example a categorie can be restaurant (out of the given list of categories) then a value "
        "of asian restaurant needs to be matched to this restaurant categorie. So as response you answer"
        "restaurant. If you don't have any good match with the categories, then answer with None. Do not "
        "answer any other text or explaination, just the categorie name or None. "
        "The categories: " + str(categories) + f". The value: + {candidate.model_dump()}."
    )
    label = resp.text.replace("`", "").replace("python", "").replace("\n", "")

    return label
