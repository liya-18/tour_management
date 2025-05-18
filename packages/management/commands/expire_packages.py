from django.core.management.base import BaseCommand
from django.utils import timezone
from packages.models import TourPackage

class Command(BaseCommand):
    help = 'Mark expired packages as expired'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        expired_packages = TourPackage.objects.filter(expiry_date__lt=today, is_expired=False)
        count = expired_packages.update(is_expired=True)
        self.stdout.write(f'{count} packages marked as expired.')
