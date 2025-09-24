from fastapi import APIRouter, Form, Depends
from typing import Annotated
from dependencies.authn import is_authenticated
from utils import genai_client


# create genai router
genai_router = APIRouter(tags=["GenAI"])


# define endpoints
@genai_router.post("/genai/generate_text", dependencies=[Depends(is_authenticated)])
def generate_text(prompt=Annotated[str, Form()]):
    response = genai_client.models.generate_content(
        model="genai-2.5-flash",
        contents=prompt,
    )
    return {"content": response.text}
