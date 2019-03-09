from django.conf.urls import url

from . import views

app_name = 'tours'

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),
    url(r'^createform/$', views.TourCreateForm.as_view(), name='tour_f'),
    url(r'^create/$', views.TourCreate.as_view(), name='tour_form'),

    url(r'^destination/$', views.Destination.as_view(), name='destination'),
    url(r'^detail/(?P<slug>[-\w]+)/$',views.TourDetail.as_view(),name='tour_detail'),
    url(r'^comment/(?P<slug>[-\w]+)/$',views.CreateComment.as_view(),name='comment'),
    url(r'^delcomment/(?P<slug>[-\w]+)/(?P<pk>[-\w]+)/$',views.DeleteComment.as_view(),name='del_comment')

]
