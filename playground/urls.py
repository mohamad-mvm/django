from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.home, name='home'),
    path('database_relational/', views.database_relational),
    path('Aggregating/', views.Aggregating),
    path('Annotate/', views.annotate),
    path('Database_Functions/', views.Database_Functions),
    path('Grouping_Data/', views.Grouping_Data),
    path('Expression_Wrappers/', views.Expression_Wrappers),
    path('Querying_Generic_Relationships/', views.Querying_Generic_Relationships),
    path('Creating_Objects/', views.Creating_Objects),
    path('Updating_Objects/', views.Updating_Objects),
]
