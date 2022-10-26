from transformers import pipeline

TOXICITY_DETECTION_MODEL_NAME = "unitary/toxic-bert"
TOXICITY_DETECTION_MODEL = pipeline('text-classification', model=TOXICITY_DETECTION_MODEL_NAME,
                                    tokenizer=TOXICITY_DETECTION_MODEL_NAME)


def predict_toxicity(text: str) -> dict:
    results_list = TOXICITY_DETECTION_MODEL({"text": text}, top_k=6)
    results = {}
    for result in results_list:
        results[result['label']] = result['score']
    return results
