from datetime import datetime
from typing import Self

from app.database.session import Session
from app.database.repositories.habit import HabitRepository
from app.database.models import Habit

class HabitsService:
    def __init__(self, habit_repositories: HabitRepository):
        self._habit_repository = habit_repositories

    @classmethod
    def init_app(cls, session: Session) -> Self:
        return cls(
            habit_repositories=HabitRepository(session)
        )

    def create_habit(self, user_id: int, name_habit: str, date_start: datetime) -> Habit:
        return self._habit_repository.create(user_id=user_id,
                                            name_hubit=name_habit,
                                            date_start=date_start)

    def get_habit(self, habit_id: int) -> Habit | None:
        return self._habit_repository.get_habit_by_id(habit_id=habit_id)

    def delete_habit(self, habit_id: int) -> bool:
        return self._habit_repository.delete_habit(habit_id=habit_id)

    def habit_update(self, habit_id: int, name_habit: str, date_start: datetime) -> bool:
        return self._habit_repository.habit_update(habit_id=habit_id,
                                                  name_habit=name_habit,
                                                  date_start=date_start)

    def get_habits_by_user_id(self, user_id: int) -> list[Habit]:
        return self._habit_repository.get_habits_by_user_id(user_id=user_id)
