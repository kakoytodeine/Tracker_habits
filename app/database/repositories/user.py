import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database.models import User
from app.database.repositories.exceptions import UserError

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self,
               tg_id: int,
               first_name: str,
               last_name: str,
               username: str) -> User:
        try:
            new_user = User(tg_id=tg_id,
                            first_name=first_name,
                            last_name=last_name,
                            username=username)
            self.session.add(new_user)
            self.session.commit()
            return new_user
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Database error while creating user: {e}')
            raise UserError('Database error while creating user')

    def delete(self, user_id: int) -> bool:
        try:
            user = self.session.query(User).filter(User.id == user_id).first()
            if user:
                self.session.delete(user)
                self.session.commit()
                return True

        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Database error while deleting user: {e}')
            raise UserError('Database error while deleting user')


    def get_user_by_tg_id(self, tg_id: int) -> User | None:
        try:
            user = self.session.query(User).filter(User.tg_id == tg_id).first()
            return user
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Database error while getting user by tg_id: {e}')
            raise UserError('Database error while getting user by tg_id')





