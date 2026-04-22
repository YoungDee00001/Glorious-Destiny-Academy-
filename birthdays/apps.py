from django.apps import AppConfig
import threading

class BirthdaysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'birthdays'

    def ready(self):
        from birthdays.background import start_birthday_scheduler
        threading.Thread(target=start_birthday_scheduler, daemon=True).start()
