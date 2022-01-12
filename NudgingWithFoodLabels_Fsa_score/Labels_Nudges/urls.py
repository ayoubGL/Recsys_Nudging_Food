
from os import name
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.conf.urls import handler404, handler500

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


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.error_404
handler500 = views.error_500