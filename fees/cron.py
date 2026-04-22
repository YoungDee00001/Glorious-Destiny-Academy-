# cron.py
"""
Django-Cron job for automatic fee reminders
Place this file in your fees app directory
"""

from django_cron import CronJobBase, Schedule
from .services import FeeReminderService
from django.utils import timezone


class FeeReminderCronJob(CronJobBase):
    """
    Cron job that runs daily to check fees and send reminders
    """
    RUN_EVERY_MINS = 1440  # Run once per day (1440 minutes = 24 hours)
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'fees.fee_reminder_cron'  # Unique code for this cron job
    
    def do(self):
        """Execute the fee reminder check"""
        print(f"[{timezone.now()}] Starting fee reminder check...")
        
        results = FeeReminderService.check_and_send_reminders()
        
        # Log results
        total_sent = results['due_soon'] + results['due_today'] + results['overdue']
        
        message = f"""
Fee Reminder Cron Job Completed
================================
Due Soon Reminders: {results['due_soon']}
Due Today Reminders: {results['due_today']}
Overdue Reminders: {results['overdue']}
Total Sent: {total_sent}
Errors: {len(results['errors'])}
Time: {timezone.now()}
        """
        
        print(message)
        
        if results['errors']:
            print("Errors encountered:")
            for error in results['errors']:
                print(f"  - {error}")
        
        return message