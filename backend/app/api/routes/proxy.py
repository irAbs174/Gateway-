from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.models import Provider, Credential
from app.core.security import decrypt_data
import httpx
from loguru import logger

router = APIRouter(prefix="/proxy", tags=["proxy"])

@router.post("/")
async def proxy_request(provider_name: str, path: str, method: str = "GET", body: dict | None = None, session: AsyncSession = Depends(get_session)):
    provider = await session.scalar(
        Provider.__table__.select().where(Provider.name == provider_name)
    )
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    credential = await session.scalar(
        Credential.__table__.select().where(Credential.provider_id == provider.id)
    )
    token = decrypt_data(credential.token_encrypted)
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        url = f"{provider.base_url.rstrip('/')}/{path.lstrip('/')}"
        response = await client.request(method, url, json=body, headers=headers)
        logger.info(f"Proxy {method} {provider_name} -> {response.status_code}")
        return {"status_code": response.status_code, "data": response.json()}
