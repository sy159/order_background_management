import os, django
from django.db.models import Count

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orange_web.settings")
    django.setup()
    from orange_manage import models
    ret = models.Admin.objects.filter(id=2).values("pwd")
    lll = models.Admin.objects.values('pwd').annotate(num=Count("pwd")).values('pwd', 'num')
