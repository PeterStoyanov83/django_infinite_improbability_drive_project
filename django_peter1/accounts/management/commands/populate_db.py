import random
from faker import Faker
from django_peter1.accounts.models import UserMaster, Course, Participant, RoomResource, Lecturer
from django.utils import timezone
from django.core.management.base import BaseCommand
import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_peter1.settings')
django.setup()


class Command(BaseCommand):
    help = "Populate the database with sample data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Populate UserMaster
        for _ in range(3):
            UserMaster.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                location=random.choice(['Workshop', 'Cocotte', 'Meal Service', 'Office Center', 'Academy']),
                pedagogical_contact=fake.name(),
                coaching_contact=fake.name(),
                program_type=fake.word()
            )

        # Populate Courses
        for _ in range(10):
            Course.objects.create(
                name=fake.sentence(nb_words=3),
                description=fake.text(),
                platform=random.choice(['Online', 'In-person']),
                category=fake.word(),
                duration=timezone.timedelta(days=random.randint(1, 60)),
                costs=fake.pydecimal(left_digits=3, right_digits=2, positive=True)
            )

        # Populate Participants
        for _ in range(50):
            Participant.objects.create(
                full_name=fake.name(),
                id_number=fake.unique.bothify(text='##??##'),
                date_of_entry=fake.past_date(),
                signed_agreement=fake.boolean(),
                period_of_stay=random.choice(['3 months', '6 months'])
            )

        # Populate RoomResource
        for i in range(50):  # Adjust the range for the number of records you want
            room = RoomResource(
                room_name=f'Room {i + 1}',
                seats_available=random.randint(5, 50),
                module=f'Module {i + 1}'  # Replace with actual module data
            )
            room.save()

        # Populate Lecturer
        for _ in range(20):
            lecturer = Lecturer.objects.create(
                full_name=fake.name(),
                bio=fake.text()
            )
            courses = Course.objects.order_by('?')[:random.randint(1, 5)]
            lecturer.courses_responsible.set(courses)

        self.stdout.write(self.style.SUCCESS('Database populated with sample data.'))
