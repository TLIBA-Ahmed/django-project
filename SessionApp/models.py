from django.db import models
from ConferenceApp.models import Conference
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


room_valid = RegexValidator(r"^[A-Za-z0-9\s\-]+$", "Room name can only contain letters, numbers, spaces, and hyphens.")

# Create your models here.
class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=100)
    session_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, validators=[room_valid])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    conference = models.ForeignKey(
        Conference, on_delete=models.CASCADE, related_name="sessions"
    )
    def clean(self):
       if self.conference:
         if not (self.conference.start_date <= self.session_date <= self.conference.end_date):
            raise ValidationError('Session date must be within the conference dates.')
         if self.end_time < self.start_time:
            raise ValidationError('End time cannot be earlier than start time.')

    



"""

from django.db import models
from UserApp.models import User
from django.core.validators import MinLengthValidator,FileExtensionValidator, RegexValidator
from django.utils import timezone
from django.forms import ValidationError
# Create your models here.
# Create your models here.
name_validator=RegexValidator(
    regex=r'^[a-zA-Z\s]+$', 
    message="The conference title must contain only letters and spaces."
    )
class Conference(models.Model):
    conference_id= models.AutoField(primary_key=True)
    name= models.CharField(max_length=200,validators=[name_validator])
    THEME_CHOICES = [
        ("AI","computer science & Artificial intelligence"),#("cle", "valeur")
        ("SE", "Science & Engineering"),
        ("SSE", "Social Sciences & Education"),
        ("INT", "interdisciplinary Themes"),

    ]
    theme= models.CharField(max_length=200, choices=THEME_CHOICES)#choices liste deroulante
    location= models.CharField(max_length=200)
    start_date= models.DateField()
    end_date= models.DateField()
    description= models.TextField(validators=[MinLengthValidator(30,"Description must be at least 30 characters long.")])#TextField pour les textes longs
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    def __str__(self)-> str:
        return f"{self.name}"
    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("End date cannot be earlier than start date.")
        if self.start_date <= timezone.now().date():
            raise ValidationError("The conference start date must be in the future.")
        

class OrganizingCommittee(models.Model):
    conference= models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='committees')#related_name='committees' = le nom que tu utilises quand tu veux aller de la conférence vers ses comités associés.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='committees')#Ça crée un raccourci sur le modèle User. te donne la liste de tous les OrganizingCommittee où cet utilisateur est présent (Chair, Co-chair, Member, etc.).
    committee_role= models.CharField(max_length=100, choices=[('Chair', 'Chair'), ('Co-Chair', 'Co-Chair'), ('Member', 'Member')], default='Member')
    date_joined= models.DateField(auto_now_add=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

def split_keywords(value):
    if len(value.keywords.split(',')) > 10:
        raise ValidationError("keywords cannot exceed 10.")
class Submission(models.Model):
    conference= models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    title= models.CharField(max_length=200)
    abstract= models.TextField()
    keywords= models.CharField(max_length=200, validators=[split_keywords])#keywords sont séparés par des virgules
    paper_file= models.FileField(upload_to='submissions/', validators=[FileExtensionValidator(allowed_extensions=["pdf"])])#FileField pour les fichiers. upload_to spécifie le répertoire où les fichiers seront stockés.
    status= models.CharField(max_length=50, choices=[('Submitted', 'Submitted'), ('Under Review', 'Under Review'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Submitted')
    submission_date= models.DateTimeField(auto_now_add=True)#Django remplit ce champ automatiquement au moment de la création de l’objet, et il ne bougera plus jamais après.affichera la date et l’heure exactes où l’objet Submission a été créé dans la base.
    payed= models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f"{self.title}"
    def clean(self):
        if (timezone.now().date()> self.conference.start_date):
            raise ValidationError('Submission date must be before the conference date.')
        today = timezone.localdate()
        count = Submission.objects.filter(
            user=self.user,
            submission_date=today
        ).exclude(pk=self.pk).count()
        if count >= 3:
            raise ValidationError('You can only submit 3 papers per day.')
        
        """