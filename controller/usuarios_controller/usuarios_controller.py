from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, EmailStr, constr
from model.usuarios_model import usuarios_model

router = APIRouter()

class usuario_base(BaseModel):
    nome_usuario: constr (min_length=3, max_length=50)
    email_usuario: EmailStr
    senha_usuario: constr (min_length=8, max_length=20)

@router.get("/")