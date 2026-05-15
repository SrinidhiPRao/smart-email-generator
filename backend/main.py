import json
import re
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator
from fastapi.middleware.cors import CORSMiddleware

from backend.services.llm_service import get_llm
from backend.services.prompt_factory import PromptFactory

from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="Smart Email Generator", version="1.0.0")

# 1. Define the origins that are allowed to talk to your API
# Add the URL/port where your React app is running
origins = [
    "http://localhost:3000",  # Default React port
    "http://localhost:5173",  # Default Vite + React port
]

# 2. Add the middleware to your FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or use ["*"] to allow all (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, etc.
    allow_headers=["*"],  # Allows all headers
)


prompt_factory = PromptFactory()
llm = get_llm()

EmailStyle = Literal["corporate", "friendly", "sales"]
AllowedTone = Literal[
    "formal", "friendly", "assertive", "empathetic", "professional", "casual"
]


class BaseEmailRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    prompt: str = Field(..., min_length=5)
    tone: AllowedTone
    recipient_name: str | None = None
    sender_name: str | None = None
    additional_context: str | None = None

    @field_validator("recipient_name", "sender_name")
    @classmethod
    def validate_names(cls, value: str | None) -> str | None:
        if value is not None and len(value) < 2:
            raise ValueError("Name fields must be at least 2 characters long.")
        return value


class EmailRequest(BaseEmailRequest):
    style: EmailStyle


class SubjectRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email_body: str = Field(..., min_length=10)
    tone: AllowedTone
    style: EmailStyle
    context: str | None = None


class ReplyRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    original_email: str = Field(..., min_length=10)
    reply_goal: str = Field(..., min_length=5)
    tone: AllowedTone
    style: EmailStyle
    recipient_name: str | None = None
    sender_name: str | None = None
    additional_context: str | None = None

    @field_validator("recipient_name", "sender_name")
    @classmethod
    def validate_names(cls, value: str | None) -> str | None:
        if value is not None and len(value) < 2:
            raise ValueError("Name fields must be at least 2 characters long.")
        return value


def parse_json_response(content: str | list) -> dict:
    """Gemini may occasionally wrap JSON in extra text, so this keeps responses stable."""
    if isinstance(content, list):
        content = "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        )

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise HTTPException(
                status_code=500, detail="Model did not return valid JSON."
            )
        return json.loads(match.group(0))


def run_prompt(system_prompt: str, user_prompt: str) -> dict:
    response = llm.invoke(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ]
    )
    return parse_json_response(response.content)


def build_email_response(payload: BaseEmailRequest, style: EmailStyle) -> dict:
    system_prompt = prompt_factory.build_email_system_prompt(
        tone=payload.tone,
        style=style,
    )
    user_prompt = prompt_factory.build_email_user_prompt(
        prompt=payload.prompt,
        tone=payload.tone,
        style=style,
        recipient_name=payload.recipient_name,
        sender_name=payload.sender_name,
        additional_context=payload.additional_context,
    )
    result = run_prompt(system_prompt, user_prompt)
    return {
        "subject": result["subject"],
        "body": result["body"],
        "tone": payload.tone,
        "style": style,
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate-email")
def generate_email(payload: EmailRequest) -> dict:
    return build_email_response(payload, payload.style)


@app.post("/generate-email/corporate")
def generate_corporate_email(payload: BaseEmailRequest) -> dict:
    return build_email_response(payload, "corporate")


@app.post("/generate-email/friendly")
def generate_friendly_email(payload: BaseEmailRequest) -> dict:
    return build_email_response(payload, "friendly")


@app.post("/generate-email/sales")
def generate_sales_email(payload: BaseEmailRequest) -> dict:
    return build_email_response(payload, "sales")


@app.post("/generate-subject")
def generate_subject(payload: SubjectRequest) -> dict:
    system_prompt = prompt_factory.build_subject_system_prompt(
        tone=payload.tone,
        style=payload.style,
    )
    user_prompt = prompt_factory.build_subject_user_prompt(
        email_body=payload.email_body,
        tone=payload.tone,
        style=payload.style,
        context=payload.context,
    )
    result = run_prompt(system_prompt, user_prompt)
    return {
        "subject": result["subject"],
        "tone": payload.tone,
        "style": payload.style,
    }


@app.post("/generate-reply")
def generate_reply(payload: ReplyRequest) -> dict:
    system_prompt = prompt_factory.build_reply_system_prompt(
        tone=payload.tone,
        style=payload.style,
    )
    user_prompt = prompt_factory.build_reply_user_prompt(
        original_email=payload.original_email,
        reply_goal=payload.reply_goal,
        tone=payload.tone,
        style=payload.style,
        recipient_name=payload.recipient_name,
        sender_name=payload.sender_name,
        additional_context=payload.additional_context,
    )
    result = run_prompt(system_prompt, user_prompt)
    return {
        "subject": result["subject"],
        "body": result["body"],
        "tone": payload.tone,
        "style": payload.style,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
