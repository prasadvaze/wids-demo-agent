import logging
import traceback
import uuid
from typing import Any, Dict

from fastapi import Depends, HTTPException
from langchain_core.messages import HumanMessage

from agents.chatbot.graph import ChatbotGraph
from api import create_app
from api.config import get_settings, Settings
from api.models.chat import ChatRequest, ChatResponse


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = create_app()


@app.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
