from django.contrib import admin
from shel.models import *
# Register your models here.
admin.site.register(Group)
admin.site.register(Person)
admin.site.register(Membership)
admin.site.register(Post)
admin.site.register(visitedPost)