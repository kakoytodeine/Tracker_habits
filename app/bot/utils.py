def correct_habit(habit) -> bool:
    if not habit or not isinstance(habit, str):
        return False
    habit = habit.strip()
    return 6 <= len(habit) <= 100 and any(c.isalnum() for c in habit)
