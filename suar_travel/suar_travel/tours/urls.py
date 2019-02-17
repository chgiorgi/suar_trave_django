from django.conf.urls import url

from . import views

app_name = 'tours'

urlpatterns = [
	url(r'^$', views.Home.as_view(), name='index'),
	url(r'^create/$', views.TourForms.as_view(), name='tour_form'),
	url(r'^create-tour/$', views.TourCreate.as_view(), name='save_tour')
]
