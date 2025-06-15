from fastapi import FastAPI, Request, WebSocket
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from router.usuarios_router import router as usuario_router
from router.produto_route import router as produto_router
from router.ws_router import router as ws_router
from router.notificacao_router import router as notificacao_router
from database.db_model import DBModel
from db_setup import criar_banco_de_dados, criar_tabelas
from controller.produtos_controller.produtos_controller import iniciar_coleta_email_controller
import asyncio

app = FastAPI()

# Middleware de Sessão
app.add_middleware(SessionMiddleware, secret_key="g464g6f84gg84x64gfdxgg8h486h468ty46h8t4t8f4g6d4g8f68dgf46gd8f4")

# Middleware CORS para liberar requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tratamento de erro de validação
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"Erro de validação: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

# Ações executadas ao iniciar o servidor
@app.on_event("startup")
async def startup():
    db_config = DBModel.get_dotenv_create_db()
    print(f"🔧 Iniciando com banco: {db_config.database}")
    criar_banco_de_dados()
    criar_tabelas()

# Rota inicial
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Produtos!"}

# Registro das rotas
app.include_router(usuario_router, tags=["Usuários"])
app.include_router(produto_router, tags=["Produtos"])
app.include_router(ws_router)
app.include_router(notificacao_router, tags=["Notificações"])

# Tarefa periódica para verificar e-mails
async def tarefa_periodica_email():
    while True:
        print("⌛ Verificando e-mails automaticamente...")
        try:
            iniciar_coleta_email_controller()
            print("✅ Coleta de e-mails concluída.")
        except Exception as e:
            print(f"❌ Erro ao coletar e-mails automaticamente: {e}")
        await asyncio.sleep(1800)  # Executa a cada 30 minutos

# Execução direta
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
