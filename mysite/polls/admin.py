from django.contrib import admin

from .models import Question

# Register your models here.
# Pollsアプリをadminページ上で編集できるようにする
admin.site.register(Question)

