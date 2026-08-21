from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

with open("knowledge.txt", "r", encoding="utf-8") as file:
    knowledge = file.read()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "Ocean chatbot is running!"}


@app.post("/chat")
def chat(request: ChatRequest):
    question = request.message.lower()

    words = question.split()

    relevant_sentences = []

    for sentence in knowledge.split("."):
        sentence_lower = sentence.lower()

        if any(word in sentence_lower for word in words if len(word) > 3):
            relevant_sentences.append(sentence.strip())

    if relevant_sentences:
        answer = ". ".join(relevant_sentences[:3]) + "."
    else:
        answer = "I couldn't find an answer to that in my knowledge."

    return {"answer": answer}