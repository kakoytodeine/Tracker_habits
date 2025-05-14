from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID Users')
    tg_id = Column(BigInteger, unique=True, nullable=False, comment='ID Telegram')
    first_name = Column(String(64), nullable=True, comment='Name user')
    last_name = Column(String(64), nullable=True, comment='Surname user')
    username = Column(String(64), nullable=False, comment='login by user')

    habits = relationship('Habit', back_populates='user')


class Habit(Base):
    __tablename__ = 'habits'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID Habit')
    user_id = Column(ForeignKey('users.id'), nullable=False, comment='ID Users')
    name_habit = Column(String(128), nullable=False, comment='Name Habit')
    date_start = Column(DateTime, nullable=False, comment='Date start')

    user = relationship('User', back_populates='habits')
    checkins = relationship('Checkin', back_populates='habit')


class Checkin(Base):
    __tablename__ = 'checkins'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID Checkin')
    habit_id = Column(ForeignKey('habits.id'), nullable=False, comment='ID Habit')
    date_checkin = Column(DateTime, nullable=False, comment='Date checkin')
    done = Column(Boolean, nullable=False, comment='Done checkin')

    habit = relationship('Habit', back_populates='checkins')

