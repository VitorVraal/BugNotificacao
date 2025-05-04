from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from model.usuarios_model.usuarios_model import (
    cadastrar_usuario,
    excluir_usuario_id,
    alterar_usuario,
    listar_usuarios,
    fazer_login
)

router = APIRouter()

# Modelo Pydantic para entrada de dados
class Usuario(BaseModel):
    nome_usuario: str
    email_usuario: EmailStr
    senha_usuario: str
    tipo_conta: int

class UsuarioUpdate(BaseModel):
    id_usuario: int
    nome_usuario: str
    email_usuario: EmailStr
    senha_usuario: str

class Login(BaseModel):
    email_usuario: EmailStr
    senha_usuario: str

@router.post("/usuarios", status_code=201)
def criar_usuario(usuario: Usuario):
    try:
        cadastrar_usuario(usuario.nome_usuario, usuario.email_usuario, usuario.senha_usuario, usuario.tipo_conta)
        return {"mensagem": "Usuário cadastrado com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/usuarios", response_model=List[dict])
def listar():
    usuarios = listar_usuarios()
    return usuarios

@router.delete("/usuarios/{id}")
def deletar_usuario(id: int):
    excluir_usuario_id(id)
    return {"mensagem": f"Usuário com ID {id} excluído com sucesso."}

@router.put("/usuarios")
def atualizar(usuario: UsuarioUpdate):
    alterar_usuario(usuario.id_usuario, usuario.nome_usuario, usuario.email_usuario, usuario.senha_usuario)
    return {"mensagem": f"Usuário com ID {usuario.id_usuario} atualizado com sucesso."}

@router.post("/login")
def login(dados: Login):
    usuario = fazer_login(dados.email_usuario, dados.senha_usuario)
    if usuario:
        return usuario
    raise HTTPException(status_code=401, detail="Credenciais inválidas.")


