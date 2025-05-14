import datetime

from app.database.session import Session
from app.database.repositoryes.user import UserRepository
from app.database.repositoryes.habit import HabitRepository

session = Session()

repo_user = UserRepository(session)
repo_habit = HabitRepository(session)

new_habit = repo_habit.get_habits_by_user_id(3)
for habit in new_habit:
    print(habit.name_habit, habit.date_start)