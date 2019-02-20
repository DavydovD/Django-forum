from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'forum'

# handler404 = 'views.handler404'

urlpatterns = [
    re_path(r'^$', views.categories, name='home'),
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^logout/$', views.logout, name='logout'),
    re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^create-category/$', views.create_category, name='create_category'),
    re_path(r'^(?P<category>[\w\s-]+)/$', views.subcategories, name='subcategories'),
    re_path(r'^(?P<category>[\w\s-]+)/create-subcategory/$', views.create_subcategory, name='create_subcategory'),
    re_path(r'^(?P<category>[\w\s-]+)/(?P<subcategory>[\w\s-]+)/create-topic/$', views.create_topic, name='create_topic'),
    re_path(r'^(?P<category>[\w\s-]+)/(?P<subcategory>[\w\s-]+)/$', views.topics, name='topics'),
    re_path(r'^(?P<category>[\w\s-]+)/(?P<subcategory>[\w\s-]+)/(?P<topic>[\w\s-]+)/$', views.topic, name='topic'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

