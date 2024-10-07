from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def test():
    return {"message": "こんにちは"}

# uvicorn main:app --reload --port 5000