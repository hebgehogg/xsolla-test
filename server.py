import logging
import uvicorn

from fastapi import FastAPI, Request
from pydantic import BaseSettings
from sqlalchemy import text
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.asyncio import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    sqlite_config: str

    class Config:
        env_file = ".env"


settings = Settings()

app = FastAPI()

engine = engine.create_async_engine(settings.sqlite_config, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@app.post("/api/create")
async def create(request: Request, session: AsyncSession = Depends(get_session)):
    sql_text = f"""
            select * from meetings
        """
    sql_text = text(sql_text)
    try:
        res = await session.execute(sql_text)
        await session.commit()
        logger.info(res.all())
        return await request.json()
    except Exception as ex:
        logger.info(ex)


@app.get("/api/update/{meeting_id}")
async def update(meeting_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    # Метод изменяет все данные встречи по ее уникальному идентификатору.
    sql_text = f"""
            select * from meetings
        """
    sql_text = text(sql_text)
    try:
        res = await session.execute(sql_text)
        await session.commit()
        logger.info(res.all())
        return await request.json()
    except Exception as ex:
        logger.info(ex)


@app.get("/api/delete")
async def delete(meeting_id: int, session: AsyncSession = Depends(get_session)):
    return meeting_id


@app.get("/api/select/{meeting_id}")
async def select(meeting_id: int, session: AsyncSession = Depends(get_session)):
    return meeting_id


@app.get("/api/select")
async def select(session: AsyncSession = Depends(get_session)):
    return 400


if __name__ == "__main__":
    uvicorn.run('server:app', port=8080, reload=True)
