
from os import name
from django.contrib import admin
from django.urls import path
from . import views
app_name = "Labels_Nudges"

urlpatterns = [
    path('',views.home, name='home'),
    path('personal_info', views.personal_info, name='personal_info'),
    path('select_category',views.select_category,name='select_category'),
    # path('rate_items', views.rate_items, name='rate_items'),
    path('rate_recipes', views.rate_recipes, name='rate_recipes'),
    path('recipe_recommendations', views.recipe_recommendations, name = 'recipe_recommendations' ),
    path('choice_evaluation',views.choice_evaluation, name='choice_evaluation'),
    path('thank_u',views.thank_u, name='thank_u'),
]
