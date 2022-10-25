from datetime import datetime
from typing import List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from MessagingService.models import schemas
from MessagingService.sql_app import models
from MessagingService.sql_app.models import Message


def get_message(db: Session, message_id: int) -> Message:
    return db.query(models.Message).filter(models.Message.id == message_id).first()


def get_messages_participant(db: Session, participant: str):
    return db.query(models.Message).filter(
        (models.Message.sender == participant) or (models.Message.receiver == participant)).all()


def get_messages_by_timestamp(db: Session, participant_id: str, timestamp_from: datetime, timestamp_to: datetime) -> \
        List[Message]:
    return db.query(models.Message).filter(models.Message.timestamp >= timestamp_from,
                                           models.Message.timestamp <= timestamp_to,
                                           or_(models.Message.sender == participant_id,
                                               models.Message.receiver == participant_id)).all()


#
# def delete_message(db: Session, message_id: int):
#     return db.delete(db.query(models.Message).filter(models.Message.id == message_id).first())

def create_message(db: Session, message: schemas.Message):
    db_item = models.Message(**message.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
