from fastapi import FastAPI
from paraphrase import parahprases_from_text

app = FastAPI()

@app.get('/paraphrase')
def ParaphrasesAPI(tree: str, limit: int = 20):
    target_label = 'NP'

    paraphrases = parahprases_from_text(tree, limit, target_label) if limit != 0 else []
    return {'amount': len(paraphrases), 'paraphrases': paraphrases}