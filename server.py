import logging
import uvicorn

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
async def create(meeting: Meeting, session: AsyncSession = Depends(get_session)):
    try:
        create_request = f"""
                INSERT INTO meetings (name, start_time, end_time, emails)
                VALUES 
                ('{meeting.name}', 
                '{meeting.start_time}', 
                '{meeting.end_time}',
                "{meeting.emails}")
                returning id;
            """
        meeting_id = await get_request(create_request, session)
        logger.info(f'meeting {meeting_id} created')
        return f'meeting_id = {meeting_id}'
    except Exception as ex:
        logger.info(ex)
        return f'exception: {ex}'


@app.post("/api/update")
async def update(meeting: Meeting, session: AsyncSession = Depends(get_session)):
    try:
        check_request = f"""
            SELECT * FROM meetings
            WHERE id = {meeting.id}
            """
        check = await get_request(check_request, session)
        if check:
            update_request = f"""
                UPDATE meetings
                SET 
                    name='{meeting.name}', 
                    start_time='{meeting.start_time}', 
                    end_time='{meeting.end_time}', 
                    emails="{meeting.emails}"
                WHERE
                    id = {meeting.id}
                """
            await save_request(update_request, session)
            logger.info(f'meeting {meeting.id} updated')
            return f'meeting updated by id = {meeting.id}'
        else: return 'this meeting does not exist or has been deleted'
    except Exception as ex:
        logger.info(ex)
        return f'exception: {ex}'


@app.get("/api/delete/{meeting_id}")
async def delete(meeting_id: int, session: AsyncSession = Depends(get_session)):
    try:
        check_request = f'SELECT * FROM meetings WHERE id = {meeting_id}'
        check = await get_request(check_request, session)
        if check:
            delete_request = f'DELETE FROM meetings WHERE id = {meeting_id}'
            await save_request(delete_request, session)
            logger.info(f'meeting {meeting_id} deleted')
            return f'meeting deleted by id = {meeting_id}'
        else: return 'this meeting does not exist or has been deleted'
    except Exception as ex:
        logger.info(ex)
        return f'exception: {ex}'


@app.get("/api/select/select_count")
async def select_count(session: AsyncSession = Depends(get_session)):
    try:
        count_request = f'SELECT count(*) FROM meetings'
        count = await get_request(count_request, session)
        return count
    except Exception as ex:
        logger.info(ex)
        return f'exception: {ex}'


@app.get("/api/select/select_all/{offset}")
async def select_all(offset: int, session: AsyncSession = Depends(get_session)):
    try:
        meetings = await session.execute(text(f'SELECT * FROM meetings LIMIT 10 OFFSET {offset}'))
        await session.commit()
        return meetings.all()
    except Exception as ex:
        logger.info(ex)
        return f'exception: {ex}'


@app.get("/api/select/{meeting_id}")
async def select(meeting_id: int, session: AsyncSession = Depends(get_session)):
    try:
        select_request = f'SELECT * FROM meetings WHERE id = {meeting_id}'
        meeting = await get_request(select_request, session)
        logger.info(f'meeting {meeting_id} showed')
        return meeting
    except Exception as ex:
        logger.info(ex)
        return f'exception: {ex}'


@app.get("/api/create_table")
async def create_table(session: AsyncSession = Depends(get_session)):
    try:
        create_table_request = f"""
                    CREATE TABLE meetings (
                        id integer PRIMARY KEY,
                        name text NOT NULL,
                        start_time datatime NOT NULL,
                        end_time datatime NOT NULL,
                        emails text NOT NULL
                    )
                """
        await save_request(create_table_request, session)
        return 'table meetings created'
    except Exception as ex:
        logger.info(ex)
        return f'exception: {ex}'


async def get_request(sql_text, session):
    response = await session.execute(text(sql_text))
    await session.commit()
    return response.one()


async def save_request(sql_text, session):
    await session.execute(text(sql_text))
    await session.commit()

if __name__ == "__main__":
    uvicorn.run('server:app', port=8080, reload=True)
