import logging
import uvicorn
import time

from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseSettings
from sqlalchemy import text
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.asyncio import engine
# todo logging

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


class Meeting(BaseModel):
    id: Optional[int] = None
    name: str
    start_time: datetime
    end_time: datetime
    emails: List[str]


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@app.post("/api/create")
async def create(body: Meeting, session: AsyncSession = Depends(get_session)):
    print(body)
    sql_text = f"""
            insert into meetings (name, start_time, end_time, emails)
            values 
            ('{body.name}', 
            '{body.start_time}', 
            '{body.end_time}',
            "{body.emails}")
            returning id;
        """

    meeting_id = await session.execute(text(sql_text))
    await session.commit()
    return meeting_id.all()


@app.post("/api/update")
async def update(body: Meeting, session: AsyncSession = Depends(get_session)):
    sql_text = f"""
            UPDATE meetings
            SET 
                name='{body.name}', 
                start_time='{body.start_time}', 
                end_time='{body.end_time}', 
                emails="{body.emails}"
            WHERE
                id = {body.id}
        """

    await session.execute(text(sql_text))
    await session.commit()
    return body.id


@app.get("/api/delete/{meeting_id}")
async def delete(meeting_id: int, session: AsyncSession = Depends(get_session)):
    # todo удалить то, чего нет))
    try:
        await session.execute(text(f"""DELETE FROM meetings WHERE id = {meeting_id}"""))
        await session.commit()
        return meeting_id
    except Exception as ex:
        logger.info(ex)


@app.get("/api/select/select_count")
async def select_count(session: AsyncSession = Depends(get_session)):
    try:
        count_request = await session.execute(text(f"""SELECT count(*) FROM meetings;"""))
        await session.commit()
        return count_request.one()
    except Exception as ex:
        logger.info(ex)


@app.get("/api/select/select_all/{offset}")
async def select_all(offset: int, session: AsyncSession = Depends(get_session)):
    try:
        meeting_data = await session.execute(text(f"""select * from meetings LIMIT 10 OFFSET {offset}"""))
        await session.commit()
        return meeting_data.all()
    except Exception as ex:
        logger.info(ex)


@app.get("/api/select/{meeting_id}")
async def select(meeting_id: int, session: AsyncSession = Depends(get_session)):
    try:
        meeting_data = await session.execute(text(f"""select * from meetings where id = {meeting_id}"""))
        await session.commit()
        return meeting_data.all()
    except Exception as ex:
        logger.info(ex)


@app.get("/api/create_table")
async def create_table(session: AsyncSession = Depends(get_session)):
    sql_text = f"""
                CREATE TABLE meetings (
                    id integer PRIMARY KEY,
                    name text NOT NULL,
                    start_time datatime NOT NULL,
                    end_time datatime NOT NULL,
                    emails text NOT NULL
                )
            """
    await session.execute(text(sql_text))
    await session.commit()


if __name__ == "__main__":
    uvicorn.run('server:app', port=8080, reload=True)
