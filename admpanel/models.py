from django.db import models

# Create your models here.
class adminUser(models.Model):
    first_name = models.TextField(null=True, max_length=20)
    last_name = models.TextField(null=True, max_length=20)
    email = models.TextField(null=False, max_length=40)
    password = models.TextField(null=False, max_length=20)

    def __str__(self):
        return self.email