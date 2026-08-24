import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai


app = FastAPI()


# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load BooksTaken knowledge
with open("knowledge.txt", "r", encoding="utf-8") as file:
    knowledge = file.read()


# Gemini client
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


class ChatRequest(BaseModel):
    message: str


SYSTEM_PROMPT = """
You are the BooksTaken assistant.

You are speaking mainly with parents and mentors.

BooksTaken helps children develop a love for reading,
curiosity, confidence, imagination, and independent thinking
through books and conversations with college mentors.

Your job is to answer questions about BooksTaken and help
parents understand the service.

IMPORTANT STYLE RULES:
- Talk like a friendly WhatsApp assistant.
- Keep answers concise and to the point.
- Usually answer in 1–3 short sentences.
- Do not give long explanations unless the user asks for more detail.
- Be warm and conversational.
- Do not sound like a formal customer-support robot.
- Ask only ONE question at a time when collecting information.
- Remember information the user has already provided.

KNOWLEDGE RULES:
- Use ONLY the BooksTaken knowledge provided below.
- Do not invent prices, features, policies, mentors, timings,
  or other information.
- If the answer cannot be found in the knowledge, say:
  "I'm not sure about that yet. I can help you with BooksTaken
  plans, sessions, mentors, and reading journeys."

BOOKING:
If the user wants to book a session, help them conversationally.

Collect information one piece at a time, such as:
- Parent's name
- Child's name
- Child's age
- Reading interests or subject
- Preferred timing

Do NOT ask for all information at once.

Do NOT claim that a booking has been completed unless
the system actually completes a booking.

BOOKSTAKEN KNOWLEDGE:
""" + knowledge


@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.post("/chat")
def chat(request: ChatRequest):

    prompt = f"""
{SYSTEM_PROMPT}

USER MESSAGE:
{request.message}

ASSISTANT:
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return {
        "answer": response.text
    }