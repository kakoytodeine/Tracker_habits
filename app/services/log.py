from datetime import date
from typing import Self

from app.database.session import Session
from app.database.repositories.habitlog import HabitLogRepository


class LogService:
    def __init__(self, habit_log_repository: HabitLogRepository):
        self._habit_log_repository = habit_log_repository

    @classmethod
    def init_app(cls, session: Session) -> Self:
        return cls(
            habit_log_repository=HabitLogRepository(session)
        )

    def mark_habit_as_done(self, habit_id: int, date_log: date) -> bool:
        return self._habit_log_repository.mark_log_as_done(habit_id=habit_id, date_log=date_log)


    def get_logs_by_habit(self, habit_id: int) -> list:
        return self._habit_log_repository.get_logs_by_habit(habit_id=habit_id)

    def get_logs_by_period(self, habit_id: int, start_date: date, end_date: date) -> list:
        return self._habit_log_repository.get_logs_by_period(habit_id=habit_id, start_date=start_date, end_date=end_date)


