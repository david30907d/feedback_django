from django.conf.urls import include, url
from django.conf.urls import patterns, url
import get_feedback

urlpatterns = patterns('get_feedback.views',
    url(r'^lottery/$', 'lottery', name='lottery'),
)