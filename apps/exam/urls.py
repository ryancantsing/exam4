from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^success', views.success),     # This line has changed!
    url(r'^wish_items$', views.wish_items),
    url(r'^create$', views.create),
    url(r'^dashboard$', views.dashboard),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^create_item$', views.create_item),
    url(r'^add_to_list$', views.add_to_list),
    url(r'^remove_from_list$', views.remove_from_list)
  ]
