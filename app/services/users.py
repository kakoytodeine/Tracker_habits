from typing import Self

from app.database.repositories.user import UserRepository
from app.database.session import Session
from app.database.models import User


class UsersService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    @classmethod
    def init_app(cls, session: Session) -> Self:
        return cls(
            user_repository=UserRepository(session)
        )

    def create_user(self, tg_id: int, first_name: str, last_name: str, username: str) -> User:
        return self._user_repository.create(tg_id=tg_id,
                                           first_name=first_name,
                                           last_name=last_name,
                                           username=username)

    def get_user_by_tg_id(self, tg_id: int) -> User | None:
        return self._user_repository.get_user_by_tg_id(tg_id=tg_id)


    def get_all_users(self) -> list[User]:
        return self._user_repository.get_all()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self._user_repository.get_user_by_id(user_id=user_id)

