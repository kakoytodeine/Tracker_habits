from datetime import date

from app.database.session import Session
from app.services.users import UsersService
from app.services.habits import HabitsService
from app.services.log import LogService

session = Session()

service_habit = HabitsService.init_app(session)
service_user = UsersService.init_app(session)
service_log = LogService.init_app(session)

def get_today_reminders() -> dict[int, list[str | None]]:
    date_now = date.today()
    all_user_habits = {}

    users = service_user.get_all_users()
    if users:
        for user in users:
            user_id = user.id
            habits = service_habit.get_habits_by_user_id(user_id=user_id)
            if habits:
                habit_names_not_done = []
                for habit in habits:
                    if not service_log.mark_habit_as_done(habit_id=habit.id, date_log=date_now):
                        habit_names_not_done.append(habit.name_habit)

                all_user_habits[user_id] = habit_names_not_done

    return all_user_habits


