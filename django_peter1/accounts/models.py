from django.db import models
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django import forms


class UserMaster(models.Model):
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    location_choices = [
        ('Workshop', 'Workshop'),
        ('Cocotte', 'Cocotte'),
        ('Meal Service', 'Meal Service'),
        ('Office Center', 'Office Center'),
        ('Academy', 'Academy')
    ]
    location = models.CharField(
        max_length=50,
        choices=location_choices
    )
    pedagogical_contact = models.CharField(  # Consider ForeignKey if it references another model
        max_length=100
    )
    coaching_contact = models.CharField(  # Consider ForeignKey if it references another model
        max_length=50
    )
    program_type = models.CharField(  # Add choices if there are specific types
        max_length=50
    )


class Course(models.Model):
    name = models.CharField(
        max_length=100
    )
    description = models.TextField(
        blank=True
    )
    platform = models.CharField(
        max_length=100,
        default='None'
    )
    category = models.CharField(
        max_length=100,
        default='None'
    )
    duration = models.DurationField(
        default=timedelta(days=30)
    )
    costs = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.name


class Participant(models.Model):
    full_name = models.CharField(
        max_length=255
    )
    id_number = models.CharField(  # or other identification ???
        max_length=100,
        unique=True
    )
    date_of_entry = models.DateField()  # Do we need that ?
    signed_agreement = models.BooleanField(
        default=False
    )
    courses_attending = models.ManyToManyField(  # shows the courses every participant is attending
        Course,
        related_name='participants'
    )
    cv_file = models.FileField(  # an option to have a CV link or file in the database
        upload_to='cvs/',
        blank=True,
        null=True,
    )
    comments = models.TextField(  # comments that are made and visible only by Lecturers/ admins
        blank=True
    )
    period_of_stay = models.CharField(  # period of stay is a choice between 3 or 6 months for the moment
        choices=[('3 months', '3 months'), ('6 months', '6 months')],
        max_length=10)

    @property
    def days_of_stay_left(self):
        months = 3 if self.period_of_stay == '3 months' else 6
        end_date = self.date_of_entry + timedelta(days=months * 30)
        today = timezone.now().date()  # Convert to date
        return (end_date - today).days if end_date > today else 0

class ParticipantForm(forms.ModelForm):
    SIGNED_AGREEMENT_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]

    signed_agreement = forms.ChoiceField(choices=SIGNED_AGREEMENT_CHOICES, widget=forms.Select())

    class Meta:
        model = Participant
        fields = ['signed_agreement']  # Include other fields here


class RoomResource(models.Model):
    room_name = models.CharField(  # could be a list of choices
        max_length=100
    )
    seats_available = models.IntegerField(default=5, validators=[
        MinValueValidator(5),
        MaxValueValidator(50)
    ])
    module = models.CharField(  # could be a list of choices
        max_length=100
    )


class Lecturer(models.Model):
    full_name = models.CharField(
        max_length=255
    )
    courses_responsible = models.ManyToManyField(
        Course,
        related_name='lecturers'
    )
    bio = models.TextField()
