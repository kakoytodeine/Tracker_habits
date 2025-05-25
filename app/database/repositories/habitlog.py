import logging

from datetime import date
from sqlalchemy.orm import Session
from app.database.models import HabitLog
from app.database.repositories.exceptions import HabitLogError
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class HabitLogRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, habit_id: int, date_log: date, done: bool = False) -> HabitLog:
        try:
            new_checkin = HabitLog(
                habit_id=habit_id,
                date_log=date_log,
                done=done
            )
            self.session.add(new_checkin)
            self.session.commit()
            return new_checkin
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Database error while creating checkin: {e}')
            raise HabitLogError('Database error while creating checkin')

    def get_log_by_date(self, habit_id: int, date_log: date) -> HabitLog | None:
        try:
            log = self.session.query(HabitLog).filter(HabitLog.habit_id == habit_id,
                                                      HabitLog.date_log == date_log).first()
            return log
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Database error while getting log by date: {e}')
            raise HabitLogError('Database error while getting log by date')

    def update_log(self, habit_id: int, date_log: date, done: bool) -> bool:
        try:
            log = self.session.query(HabitLog).filter(HabitLog.habit_id == habit_id,
                                                      HabitLog.date_log == date_log).first()
            if log:
                log.done = done
                self.session.commit()
                return True
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Database error while updating log: {e}')
            raise HabitLogError('Database error while updating log')

    def delete_log(self, habit_id: int, date_log: date) -> bool:
        try:
            log = self.session.query(HabitLog).filter(HabitLog.habit_id == habit_id,
                                                      HabitLog.date_log == date_log).filter()
            if log:
                self.session.delete(log)
                self.session.commit()
                return True
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Database error while deleting log: {e}')
            raise HabitLogError('Database error while deleting log')

    def get_logs_by_habit(self, habit_id: int) -> list[HabitLog]:
        try:
            logs = self.session.query(HabitLog).filter(HabitLog.habit_id == habit_id).all()
            return logs
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Database error while getting logs by habit_id: {e}')
            raise HabitLogError('Database error while getting logs by habit_id')

    def get_logs_by_period(self, habit_id: int, start_date: date, end_date: date) -> list[HabitLog]:
        try:
            logs = self.session.query(HabitLog).filter(HabitLog.habit_id == habit_id).filter(
                HabitLog.date_log.between(start_date, end_date)).all()
            return logs
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Database error while getting logs by period: {e}')
            raise HabitLogError('Database error while getting logs by period')

    def count_logs_by_habit(self, habit_id: int) -> int | None:
        try:
            quantity_logs = self.session.query(HabitLog).filter(HabitLog.habit_id == habit_id).count()
            return quantity_logs
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Database error while counting logs by habit_id: {e}')
            raise HabitLogError('Database error while counting logs by habit_id')

    def mark_log_as_done(self, habit_id: int, date_log: date) -> bool:
        try:
            log = self.session.query(HabitLog).filter(HabitLog.habit_id == habit_id,
                                                      HabitLog.date_log == date_log).first()
            if log:
                log.done = True
                self.session.commit()
                return True
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Database error while marking log as done: {e}')
            raise HabitLogError('Database error while marking log as done')
