import datetime
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from app.reminder.reminder_service import get_today_reminders
from app.reminder.reminder_service import service_user
from app.bot.bot import bot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def send_reminders(list_habits: dict):
    try:
        date = datetime.date.today()
        time_now = datetime.datetime.now().time()
        for user_id, habits in list_habits.items():
            user = service_user.get_user_by_id(user_id)

            if not user:
                continue

            habit_count = len(habits)
            habit_word = 'привычка' if habit_count == 1 else 'привычки' if 2 <= habit_count <= 4 else 'привычек'
            format_habits = "\n".join(f"✅ {habit}" for habit in habits)

            message_text = (
                f"Здравствуйте, {user.first_name}!\n\n"
                f"На {date:%d.%m.%Y} {time_now.strftime('%H:%M')} у вас {habit_count} {habit_word} "
                f"ожидают выполнения:\n\n"
                f"{format_habits}"
            )

            bot.send_message(user.tg_id, message_text)

    except Exception as e:
        logger.error(f"Error sending reminders: {str(e)}")

scheduler = BlockingScheduler()

scheduler.add_job(send_reminders, 'cron', args=[get_today_reminders()], hour=7, minute=0)
scheduler.add_job(send_reminders, 'cron', args=[get_today_reminders()], hour=12, minute=0)
scheduler.add_job(send_reminders, 'cron', args=[get_today_reminders()], hour=18, minute=0)
scheduler.add_job(send_reminders, 'cron', args=[get_today_reminders()], hour=21, minute=0)

if __name__ == '__main__':
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
