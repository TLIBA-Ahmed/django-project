from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import uuid

name_validator = RegexValidator(
    r"^[a-zA-Z]+$", "Only alphabetic characters are allowed."
)


def email_validator(value):
    allowed_domains = ["esprit.tn", "univ.tn", "mit.edu", "ox.ac.uk"]
    domain = value.split("@")[-1]
    if domain not in allowed_domains:
        raise ValidationError(
            f'Email domain must be one of the following: {", ".join(allowed_domains)}'
        )

def generate_user_id():
    return "USER"+uuid.uuid4().hex[:4].upper()
    
class User(AbstractUser):
    user_id = models.CharField(
        max_length=8, primary_key=True, unique=True, editable=False
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    affiliation = models.CharField(max_length=100, blank=True,null=True)
    role = models.CharField(max_length=100, choices=[('Committee', 'Committee'), ('Participant', 'Participant')], default='Participant')
    nationality = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.user_id:
            new_id = generate_user_id()
            while User.objects.filter(user_id=new_id).exists():
                new_id = generate_user_id()
            self.user_id = new_id
        super().save(*args, **kwargs)