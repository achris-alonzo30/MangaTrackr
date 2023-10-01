import schedule
import time
import pytz
from datetime import datetime

"""def my_job():
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"This job runs every day at {current_time}.")


def main():
    # Get the current local time
    current_time = datetime.now().strftime("%H:%M:%S")

    # Print the current time for reference
    print(f"Current local time is {current_time}")

    # Schedule the job to run every day at the current time
    schedule.every().day.at(current_time).do(my_job)

    # Continuously check the schedule and run the job when it's time
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
"""

for tz in pytz.all_timezones:
    print(tz)
