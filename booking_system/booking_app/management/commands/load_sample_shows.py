# booking_app/management/commands/load_sample_shows.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from booking_app.models import Show

class Command(BaseCommand):
    help = 'Loads sample shows into the database'

    def handle(self, *args, **options):
        shows_data = [
            {
                'title': 'The Dark Knight',
                'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'date_time': timezone.now() + timedelta(days=2),
                'duration': timedelta(minutes=152),
                'venue': 'Main Theater',
                'total_seats': 200,
                'price': 12.99
            },
            {
                'title': 'Inception',
                'description': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
                'date_time': timezone.now() + timedelta(days=3),
                'duration': timedelta(minutes=148),
                'venue': 'Main Theater',
                'total_seats': 200,
                'price': 14.99
            },
            {
                'title': 'Coldplay: Music of the Spheres Tour',
                'description': 'Experience Coldplay live in concert with their spectacular Music of the Spheres world tour.',
                'date_time': timezone.now() + timedelta(days=5),
                'duration': timedelta(minutes=120),
                'venue': 'Concert Hall',
                'total_seats': 5000,
                'price': 89.99
            },
            {
                'title': 'Hamilton',
                'description': 'The story of America then, told by America now. Featuring a score that blends hip-hop, jazz, R&B and Broadway.',
                'date_time': timezone.now() + timedelta(days=7),
                'duration': timedelta(minutes=160),
                'venue': 'Broadway Theater',
                'total_seats': 1500,
                'price': 129.99
            },
            {
                'title': 'Premier League: Manchester United vs Liverpool',
                'description': 'Watch the biggest rivalry in English football live at Old Trafford.',
                'date_time': timezone.now() + timedelta(days=10),
                'duration': timedelta(minutes=105),
                'venue': 'Old Trafford',
                'total_seats': 75000,
                'price': 75.00
            }
        ]

        for show_data in shows_data:
            show, created = Show.objects.get_or_create(
                title=show_data['title'],
                defaults={
                    'description': show_data['description'],
                    'date_time': show_data['date_time'],
                    'duration': show_data['duration'],
                    'venue': show_data['venue'],
                    'total_seats': show_data['total_seats'],
                    'available_seats': show_data['total_seats'],
                    'price': show_data['price']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created show: {show.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Show already exists: {show.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample shows'))