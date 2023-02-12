from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('gen', views.genRepo, name='Repo Generation'),
    path('repo/<id>/', views.repo, name="Repository"),
    path('repo/<id>/journalctl', views.repo_journalctl, name="Journal"),


    path('repo/<id>/start', views.repo_start, name=""),
    path('repo/<id>/stop', views.repo_stop, name=""),
    path('repo/<id>/enable', views.repo_enable, name=""),
    path('repo/<id>/disable', views.repo_disable, name=""),

    path('error/repodoesnotexist/', views.error_repodoesnotexist, name="Error Repo Does Not Exist"),

]