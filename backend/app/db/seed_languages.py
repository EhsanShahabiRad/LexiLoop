import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models.language import Language
from app.models.language_pair import LanguagePair
from app.core.config import settings

DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def seed_languages():
    async with AsyncSessionLocal() as session:
        existing = await session.execute(
            Language.__table__.select().limit(1)
        )
        if existing.first():
            print("🚫 Languages already seeded. Skipping.")
            return

        # Create languages
        en = Language(code="en", name="English")
        fr = Language(code="fr", name="French")
        de = Language(code="de", name="German")

        session.add_all([en, fr, de])
        await session.flush()

        # Create language pairs (English → French, English → German)
        en_fr = LanguagePair(source_lang_id=en.id, target_lang_id=fr.id)
        en_de = LanguagePair(source_lang_id=en.id, target_lang_id=de.id)

        session.add_all([en_fr, en_de])
        await session.commit()
        print("✅ Languages and language pairs seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_languages())
