import time
from datetime import datetime, timedelta

def start_birthday_scheduler(target_hour=10, target_minute=0, delay_seconds=0):
    from birthdays.utils import check_and_send_birthday_emails

    def run():
        # send for today immediately (no delay)
        check_and_send_birthday_emails(test_mode=False)

        while True:
            now = datetime.now()
            target_time = now.replace(hour=target_hour, minute=target_minute,
                                      second=0, microsecond=0)
            if now >= target_time:
                target_time += timedelta(days=1)

            time.sleep((target_time - now).total_seconds())

            # send daily email
            check_and_send_birthday_emails(test_mode=False)

    import threading
    threading.Thread(target=run, daemon=True).start()
