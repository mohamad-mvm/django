from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('database_relational/', views.database_relational),
    path('Aggregating/', views.Aggregating),
    path('Annotate/', views.annotate),
    path('Database_Functions/', views.Database_Functions),
]
