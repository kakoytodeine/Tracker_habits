import logging
from datetime import datetime

from sqlalchemy.orm import Session
from app.database.models import Habit
from app.database.repositoryes.exceptions import HabitError
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class HabitRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_id: int, name_hubit: str, date_start: datetime) -> Habit:
        try:
            new_habit = Habit(
                user_id=user_id,
                name_habit=name_hubit,
                date_start=date_start
            )
            self.session.add(new_habit)
            self.session.commit()
            return new_habit
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Database error while creating habit: {e}')
            raise HabitError('Database error while creating habit')

    def get_habits_by_user_id(self, user_id: int) -> list[Habit]:
        try:
            habits = self.session.query(Habit).filter(Habit.user_id == user_id).all()
            return habits
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Database error while getting habits by user_id: {e}')
            raise HabitError('Database error while getting habits by user_id')

