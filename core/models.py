from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class PlatformUser(AbstractUser):
    # Override the email field to make it required
    ## Dont want to make this required while developing atm
    #email = models.EmailField(unique=True, blank=False, null=False)

    # Third-Party Identifiers
    sleeper_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

