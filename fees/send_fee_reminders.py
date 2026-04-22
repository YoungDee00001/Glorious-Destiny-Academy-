# management/commands/send_fee_reminders.py
"""
Django management command to send fee reminders
Create this file at: fees/management/commands/send_fee_reminders.py

Directory structure needed:
fees/
  management/
    __init__.py  (create empty file)
    commands/
      __init__.py  (create empty file)
      send_fee_reminders.py  (this file)

Run this daily using cron or django-cron
Usage: python manage.py send_fee_reminders
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from fees.services import FeeReminderService


class Command(BaseCommand):
    help = 'Check all fees and send appropriate reminders'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without actually sending emails',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                f'Starting fee reminder check at {timezone.now()}'
            )
        )
        
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No emails will be sent')
            )
        
        # Run the reminder service
        results = FeeReminderService.check_and_send_reminders()
        
        # Display results
        self.stdout.write(
            self.style.SUCCESS(
                f"\nReminder Summary:"
            )
        )
        self.stdout.write(f"  Due Soon reminders sent: {results['due_soon']}")
        self.stdout.write(f"  Due Today reminders sent: {results['due_today']}")
        self.stdout.write(f"  Overdue reminders sent: {results['overdue']}")
        
        if results['errors']:
            self.stdout.write(
                self.style.ERROR(
                    f"\n  Errors encountered: {len(results['errors'])}"
                )
            )
            for error in results['errors']:
                self.stdout.write(self.style.ERROR(f"    - {error}"))
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\nCompleted at {timezone.now()}"
            )
        )