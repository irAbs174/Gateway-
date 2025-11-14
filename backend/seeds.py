import asyncio
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import engine, AsyncSessionLocal
from app.models import Base, Provider, Credential
from app.core.security import encrypt_data

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Provider).where(Provider.name == "test_api"))
        existing = result.scalar_one_or_none()

        if existing:
            logger.info("✅ Provider 'test_api'")
            return

        provider = Provider(name="test_api", base_url="https://httpbin.org")
        session.add(provider)
        await session.flush()

        cred = Credential(
            provider_id=provider.id,
            token_encrypted=encrypt_data("testtoken123")
        )
        session.add(cred)
        await session.commit()

        logger.info("🌱 Database seeded successfully with provider 'test_api'.")

if __name__ == "__main__":
    asyncio.run(seed())
