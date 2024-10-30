import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import httpx

logger = logging.getLogger(__name__)

app = FastAPI()
security = HTTPBasic()

usuario_valido = "admin"
senha_valida = "admin"

mock_api_url = "https://671fdaa1e7a5792f052fc4f1.mockapi.io/api/v1/names"

# Função para autenticação
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if (credentials.username != usuario_valido or
        credentials.password != senha_valida):
        logger.warning(f"Falha na autenticação: {credentials.username}")
        raise HTTPException(
            status_code=401, detail="Credenciais inválidas"
        )
    return credentials.username

@app.get("/names")
async def getNomes(credentials: HTTPBasicCredentials = Depends(authenticate)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(mock_api_url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Erro ao acessar a mock API")