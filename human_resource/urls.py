from django.conf.urls import url
from django.contrib import admin
from core import views
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^admin/', admin.site.urls),
    url(r'^select/role/', views.select_role, name='select-role'),
    url(r'^signup/(?P<role>[-\w]+)/$', views.signup, name='signup'),
    url(r'^login/', views.auth, name='login'),
    url(r'^logout', views.logout_user, name='logout'),
    url(r'^users/$', views.user_list, name='user-list'),
    url(r'^users/(?P<pk>\d+)/$', views.user_detail, name='user-detail'),
    url(r'^update/$', views.update_profile, name='update-profile'),
    url(r'^dashboard/', views.admin_dashboard, name='admin-dashboard'),
    url(r'^search/$', views.search),
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
