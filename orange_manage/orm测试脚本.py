import os, django
from django.db.models import Count
from orange_manage.models import *

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orange_web.settings")
    django.setup()
    ret = Admin.objects.filter(id=2).values("pwd")
    lll = Admin.objects.values('pwd').annotate(num=Count("pwd")).values('pwd', 'num')