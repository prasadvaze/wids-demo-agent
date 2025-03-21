from fastapi import APIRouter, Depends
from openai import AsyncOpenAI
from app.dependencies.llm import get_llm_client, get_test_chat

router = APIRouter()


@router.get("/chat")
async def chat(client: AsyncOpenAI = Depends(get_llm_client)):
    return await get_test_chat(client)
