# birthdays/management/commands/send_daily_birthday_emails.py

import time
from django.core.management.base import BaseCommand
from birthdays.utils import check_and_send_birthday_emails


class Command(BaseCommand):
    help = "Waits 10 minutes, then checks birthdays and sends emails once per day."

    def handle(self, *args, **options):
        self.stdout.write("⏳ Waiting 10 minutes before sending daily birthday emails...")
        time.sleep(600)  # 600 seconds = 10 minutes

        self.stdout.write("🎉 Sending birthday emails...")
        check_and_send_birthday_emails(test_mode=False)

        self.stdout.write("✅ Finished sending today's birthday emails.")
