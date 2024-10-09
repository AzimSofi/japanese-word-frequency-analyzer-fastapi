from fastapi import FastAPI
from pydantic import BaseModel
import MeCab
import mysql.connector

app = FastAPI()

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'japanese-word-frequency-analyzer-app',
    'port': 3306
}

mecab = MeCab.Tagger()

# Data model for incoming request
class TextData(BaseModel):
    text_id: int

# Test
@app.get("/")
def test():
    return {"message": "こんにちは"}

@app.post("/analyze")
def analyze_text(data: TextData):
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT content FROM input_texts WHERE id = {data.text_id}")
    result = cursor.fetchone()
    
    if not result:
        return {"error": "Text not found"}

    text_content = result['content']
    
    # Analyze
    node = mecab.parseToNode(text_content)
    word_freq = {}
    # Count frequencies
    while node:
        features = node.feature.split(",")
        word = node.surface
        # if features[0] == "名詞":  # Only count nouns
        word_freq[word] = word_freq.get(word, 0) + 1
        node = node.next

    # Close database connection
    cursor.close()
    conn.close()
    
    # Return JSON 
    return {"frequencies": word_freq}


# uvicorn main:app --reload --port 5000
# http://127.0.0.1:5000/docs
# http://127.0.0.1:5000/openapi.json