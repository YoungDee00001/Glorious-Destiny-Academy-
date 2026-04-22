from django.db import models


class BirthdayNotification(models.Model):
    '''Track birthday notifications sent'''
    student = models.ForeignKey('students.StudentRegistration', on_delete=models.CASCADE)
    notification_date = models.DateField(auto_now_add=True)
    message_sent = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-notification_date']
    
    def __str__(self):
        return f"Birthday notification for {self.student}"






