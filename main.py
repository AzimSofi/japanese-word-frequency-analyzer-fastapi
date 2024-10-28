from fastapi import FastAPI
from pydantic import BaseModel
import MeCab

app = FastAPI()

mecab = MeCab.Tagger()

# Test
@app.get("/")
def test():
    return {"message": "こんにちは"}

class AnalyzeTextData(BaseModel):
    content: str

@app.post("/analyze")
def analyze_text(data: AnalyzeTextData):
    text_content = data.content
    
    node = mecab.parseToNode(text_content)
    word_freq = {}

    while node:
        word = node.surface
        if word:  # Avoid empty nodes
            word_freq[word] = word_freq.get(word, 0) + 1
        node = node.next

    return {"frequencies": word_freq}

class TokenizeTextData(BaseModel):
    content: str

@app.post("/tokenize")
def tokenize_text(data: TokenizeTextData):
    text_content = data.content

    node = mecab.parseToNode(text_content)
    separated_words = []

    while node:
        word = node.surface
        if word:  # Avoid empty nodes
            separated_words.append(word)
        node = node.next

    return {"words": separated_words}

# uvicorn main:app --reload --port 5000
# http://127.0.0.1:5000/docs
# http://127.0.0.1:5000/openapi.json