"""shelegram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns
from django.contrib import admin

from shel.views import LoginView
from django.views.generic import TemplateView

from shelegram import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^index/$', 'shel.views.index_view'),
    url(r'^signup/$', 'shel.views.signup'),
    url(r'^thanks/$', 'shel.views.thanks'),
    url(r'^mainAfterLogin/', 'shel.views.main_after_login'),
    url(r'^logout/$', 'shel.views.log_out'),
     url(r'^makegrp/$', 'shel.views.make_group'),
    url(r'^karbari/$', 'shel.views.karbari'),
    url(r'^results/$', 'shel.views.search'),
    url(r'^sendrequest/$', 'shel.views.sendrequest'),
    url(r'^edit_profile/$', 'shel.views.edit_profile'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),



]