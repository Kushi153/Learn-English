from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from spellchecker import SpellChecker
from fastapi.responses import HTMLResponse
import os

# 1. INITIALIZE FASTAPI APP FIRST
app = FastAPI()

# 2. CONFIGURE CORS MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

spell = SpellChecker()

class ChatRequest(BaseModel):
    mode: str
    message: str
    personality: Optional[str] = "friendly"

# 3. DEFINE ROUTES AFTER app IS CREATED
@app.get("/", response_class=HTMLResponse)
async def serve_homepage():
    html_path = "index.html"
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "index.html not found!"

@app.post("/start")
async def start_session(
    mode: str = Form(...),
    personality: Optional[str] = Form("friendly"),
    resume_text: Optional[str] = Form(""),
    jd_text: Optional[str] = Form(""),
    resume_file: Optional[UploadFile] = File(None),
    jd_file: Optional[UploadFile] = File(None)
):
    final_resume = resume_text
    if resume_file:
        content = await resume_file.read()
        final_resume += "\n" + content.decode("utf-8", errors="ignore")

    final_jd = jd_text
    if jd_file:
        content = await jd_file.read()
        final_jd += "\n" + content.decode("utf-8", errors="ignore")

    if mode == "speaking":
        if personality == "comedy":
            greeting = "Hey! Ready for a fun chat? Throw a topic my way, or I can kick things off with a joke."
        elif personality == "serious":
            greeting = "Hello. Let's keep our conversation clear and professional. What would you like to discuss?"
        else:
            greeting = "Hey there! Great to chat with you. What's on your mind today?"
    else:
        greeting = "Hi! Let's jump right into your interview. To kick things off, can you tell me a bit about yourself and your background?"

    return {"response": greeting}

@app.post("/chat")
async def chat_with_ai(data: ChatRequest):
    user_msg = data.message.lower().strip()

    if data.mode == "speaking":
        if data.personality == "comedy":
            reply = f"Haha, seriously? '{data.message}'! That's awesome. Tell me more about that."
        elif data.personality == "serious":
            reply = f"Got it. Regarding '{data.message}', how would you analyze the core impact of that?"
        else:
            reply = f"Oh cool, '{data.message}'! That makes total sense. What happened next?"
    else:
        if "myself" in user_msg or "background" in user_msg or "graduated" in user_msg or "experience" in user_msg:
            reply = "Nice background! Out of all your past projects, which one was your favorite and why?"
        elif "project" in user_msg or "challenge" in user_msg or "built" in user_msg:
            reply = "That sounds like a solid build. How did you handle testing or bugs under tight deadlines?"
        else:
            reply = f"Makes sense. To tie that back to the role, can you give me a quick example of a time you crushed a tough goal?"

    return {"response": reply}

@app.post("/suggest-topic")
async def suggest_topic(data: ChatRequest):
    topics = [
        "Let's chat about our favorite travel spots or dream road trips.",
        "If you could learn any tech skill instantly, what would it be?",
        "What do you think is the coolest gadget or app released recently?",
        "What is a fun hobby or project you love working on in your free time?"
    ]
    import random
    return {"response": f"How about this: {random.choice(topics)}"}

@app.post("/summary")
async def get_summary(data: ChatRequest):
    if data.mode == "speaking":
        summary = "Great session! You sounded natural, kept a steady flow, and your phrasing was spot on."
    else:
        summary = "Interview wrap-up: You hit the key points well! Just remember to keep your answers concise and punchy."
    return {"response": summary} 