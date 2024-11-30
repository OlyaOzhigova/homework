from datetime import datetime
from application.salary import calculate_salary
from application.db.people import get_employees


def main():
    current_date = datetime.now().date()
    print(f"Current date: {current_date}")
    calculate_salary()
    get_employees()


if __name__ == '__main__':
    main()
