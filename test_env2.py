import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ruzo.settings')
django.setup()

from django.conf import settings
print("WAKILNI_KEY:", repr(settings.WAKILNI_KEY))
print("WAKILNI_SECRET:", repr(settings.WAKILNI_SECRET))
