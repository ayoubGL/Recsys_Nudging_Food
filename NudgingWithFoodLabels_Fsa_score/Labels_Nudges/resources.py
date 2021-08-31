from django.db import models
from import_export import resources
from .models import HealthyRecipe, UnhealthyRecipe

class HealthyRecipeResource(resources.ModelResource):
    class Meta:
        model = HealthyRecipe
class UnhealthyRecipeResource(resources.ModelResource):
    class Meta:
        model = UnhealthyRecipe