from django.conf.urls import patterns, url

from .views import StacksPageDetailView

urlpatterns = patterns(
    '',
    url(
        r'^(?P<slug>[-\w]+)/$',
        StacksPageDetailView.as_view(),
        name='stackspage-detail'
    ),
)
