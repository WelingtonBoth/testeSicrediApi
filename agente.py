import httpx
import logging
from requests.auth import HTTPBasicAuth
from typing import List, Dict
import pandas as pd
import Levenshtein

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NamesAPIClient:
    def __init__(self, base_url: str, usuario: str, senha: str):
        self.client = httpx.AsyncClient(base_url=base_url, auth=HTTPBasicAuth(usuario, senha))

    async def getNomes(self, limit: int = 10) -> List[str]:
        try:
            response = await self.client.get(f"/names?limit={limit}")
            response.raise_for_status()
            data = response.json()
            return [item['name'] for item in data[:limit]]
        except httpx.HTTPStatusError as exc:
            logger.error("Erro de status %s", exc.response.status_code)
        except httpx.RequestError as exc:
            logger.error("Erro de conexão: %s", exc)
        return []

async def main():
    api_client = NamesAPIClient("http://127.0.0.1:8000", "admin", "admin")
    nomes = await api_client.getNomes()

    if not nomes:
        logger.warning("Nenhum nome foi obtido da API.")
        return

    primeiro_nome = nomes[0]
    distances = [{"Nome": nome, "Distância para origem": Levenshtein.distance(primeiro_nome, nome)} for nome in nomes[1:]]

    df = pd.DataFrame(distances)
    df = df.sort_values(by="Distância para origem").reset_index(drop=True)

    print(f"Primeiro nome: {primeiro_nome}")
    print(df)

import asyncio
asyncio.run(main())
