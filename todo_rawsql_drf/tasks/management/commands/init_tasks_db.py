from django.core.management.base import BaseCommand
from tasks import db

class Command(BaseCommand):
    help = 'Initialize tasks sqlite DB and tables (raw SQL)'

    def handle(self, *args, **options):
        db.create_tasks_table()
        self.stdout.write(self.style.SUCCESS('Initialized tasks DB.'))
