from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Check environment variables and settings'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Environment Check:'))
        self.stdout.write(f"DEBUG: {settings.DEBUG}")
        self.stdout.write(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        self.stdout.write(f"SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}")
        self.stdout.write(f"SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
        self.stdout.write(f"CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
        self.stdout.write(f"STATIC_ROOT: {settings.STATIC_ROOT}")
        self.stdout.write(f"MEDIA_ROOT: {settings.MEDIA_ROOT}") 