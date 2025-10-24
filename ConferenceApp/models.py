from django.utils import timezone
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.validators import FileExtensionValidator
from django.forms import ValidationError
from django.core.validators import RegexValidator


conference_title_valid = RegexValidator(
    regex=r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$',
    message="Le titre de la conférence ne doit contenir que des lettres et des espaces.",
    code='invalid_conference_title'
)
    
    

conf_desc_validator = MinLengthValidator(30,'Description must be at least 30 characters long.')


# Create your models here.
class Conference(models.Model):

    THEME_CHOICES = [
        ("CSAI", "Computer Science & Artificial Intelligence"),
        ("SE", "Science & Engineering"),
        ("SSE", "Social Sciences & Education"),
        ("IT", "Interdisciplinary Themes"),
    ]
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, validators=[conference_title_valid])
    theme = models.CharField(max_length=100, choices=THEME_CHOICES)
    description = models.TextField(validators= [conf_desc_validator])
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    def __str__(self) -> str:
        return f"{self.name}"
    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError('End date cannot be earlier than start date.')


class OrganizingCommittee(models.Model):
    
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='committees')
    user = models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name='committees')


    committee_role = models.CharField(max_length=100 , choices=[('Chair', 'Chair'), ('Co-Chair', 'Co-Chair'), ('Member', 'Member')],default='Member')
    date_joined = models.DateField(auto_now_add=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def split_keywords(value):
    if (len(value.split(',')) > 10):
        raise ValidationError('Keywords must not exceed 10 words.')

class Submission(models.Model):
    conference = models.ForeignKey(
        Conference, on_delete=models.CASCADE, related_name="Submission"
    )
    user = models.ForeignKey(
        "UserApp.User", on_delete=models.CASCADE, related_name="Submission"
    )
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    keywords = models.CharField(max_length=200, validators=[split_keywords])
    paper = models.FileField(upload_to="papers/", validators=[FileExtensionValidator(allowed_extensions=["pdf"])],default='papers/default.pdf')
    status = models.CharField(
        max_length=50,
        choices=[
            ("Submitted", "Submitted"),
            ("Under Review", "Under Review"),
            ("Accepted", "Accepted"),
            ("Rejected", "Rejected"),
        ],
        default="Submitted",
    )
    submission_date = models.DateField(auto_now_add=True)
    payed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title}"
    def clean(self):
        if (timezone.localdate() > self.conference.start_date):
            raise ValidationError('Submission date must be before the conference date.')
        today = timezone.localdate()
        count = Submission.objects.filter(
            user=self.user,
            submission_date=today
        ).exclude(pk=self.pk).count()
        if count >= 3:
            raise ValidationError('You can only submit 3 papers per day.')

    

