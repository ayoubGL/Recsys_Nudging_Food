from sys import maxsize
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.enums import ChoicesMeta
from django.db.models.fields import AutoField, CharField, DateTimeField
from django.db.models.fields.related import ForeignKey
from pkg_resources import require
from .choices import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django_countries.fields import CountryField
from multiselectfield import MultiSelectField

# Create your models here.


class Personal_info(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=50,
        editable=False,
        default='Personal_info')

    created = models.DateTimeField(auto_now_add=True)

    age = models.CharField(max_length=120,
                           choices=Age_choices,
                           verbose_name='age',
                           default=None,
                           blank=False
                           )

    country = CountryField(blank_label='')

    education = models.CharField(max_length=120,
                                 choices=EducationLevel,
                                 verbose_name='education',
                                 default=None,
                                 blank=False

                                 )

    diet_restriction = MultiSelectField(
        choices=DietRestrictions,
        verbose_name='DietRestrictions',
        blank=False,
        # default= None,
    )

    diet_goal = MultiSelectField(
        choices=DietGoal,
        verbose_name='DietGoals',
        blank=False,

        # default=None
    )

    cooking_exp = models.CharField(max_length=300,
                                   choices=CookingExprience,
                                   verbose_name='cooking_exp',
                                   default=None,
                                   blank=False
                                   )
    eating_habits = models.CharField(max_length=300,
                                     choices=EatingHabit,
                                     verbose_name='eating_habits',
                                     blank=False,
                                     default=None,
                                     )

    gender = models.CharField(max_length=300,
                              choices=Gender_choices,
                              verbose_name='gender',
                              default=None,
                              blank=False
                              )

    session_id = models.CharField(max_length=1000, blank=False, default=None)

    class Meta:
        verbose_name = 'personal_info'
        ordering = ['id']
        db_table = 'personal_info'

    def __str__(self):
        return "{}".format(self.id)


class FoodCategory(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey(
        Personal_info,
        on_delete=models.CASCADE
    )

    category = models.CharField(("Category"),
                                max_length=50,
                                choices=foodCategories,
                                blank=False,
                                default=None)
    created = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=1000, blank=False, default=None)

    class Meta:
        verbose_name = 'FoodCategory'
        ordering = ['id']
        db_table = 'FoodCategory'

    # def __str__(self):
    #     return "{}".format(self.person)


# class Recipes(models.Model):
#     id = models.AutoField(primary_key=True)
#     URL = models.CharField(("URL"), max_length=500, blank=False)
#     Name = models.CharField(("Name"), max_length=300)
#     category = models.CharField(("category"), max_length=500)
#     Size = models.CharField('Size', max_length=200)
#     Serving = models.CharField(("Servings"), max_length=200)
#     Calories = models.CharField(("Calories"), max_length=200)
#     # AverageRatings = models.CharField('AverageRatings', max_length=200)
#     # Ratings = models.CharField(("Ratings"), max_length=200)
#     image_link = models.CharField(("image"), max_length=500)

#     class Meta:
#         verbose_name = 'Recipes'
#         ordering = ['id']
#         db_table = 'Recipes'
#     def __str__(self):
#         return self.Name
    # def __unicode__(self):
    #     return  self.Name
#     # created = models.DateTimeField(auto_now_add=True)


    #   l = ['id','URL','Name','fiber_g','sodium_g','carbohydrates_g','fat_g','protein_g','sugar_g','saturate_g', 'size_g','Servings',
    #               'calories_kCal','category','image_link','fat_100g','fiber_100g','sugar_100g','saturated_100g','protien_100g','sodium_100mg',  
    #               'carbohydrates_100g','kj_100g','Nutri_score','Fsa_new','salt_100g','salt_g','fat_count','satfat_count','sugar_count','salt_count'] 

class HealthyRecipe(models.Model):
    id = models.AutoField(primary_key=True)
    URL = models.CharField(max_length=300)
    Name = models.CharField( max_length=500)
    fiber_g = models.CharField( max_length=50)
    sodium_g = models.CharField( max_length=50)
    carbohydrates_g= models.CharField(max_length=50)
    fat_g = models.CharField(max_length=50)
    protein_g = models.CharField(max_length=50)
    sugar_g= models.CharField( max_length=50)
    saturate_g = models.CharField(max_length=50)
    size_g = models.CharField( max_length=50)
    Servings = models.CharField( max_length=50)
    calories_kCal =  models.CharField( max_length=50)
    category = models.CharField( max_length=50)
    image_link = models.CharField( max_length=500)
    fat_100g = models.CharField( max_length=50)
    fiber_100g = models.CharField(max_length=50)
    sugar_100g = models.CharField( max_length=50)
    saturated_100g = models.CharField( max_length=50)
    protien_100g = models.CharField( max_length=50)
    sodium_100mg = models.CharField(max_length=50)
    carbohydrates_100g = models.CharField(max_length=50)
    kj_100g = models.CharField( max_length=50)
    Nutri_score  = models.CharField( max_length=50)
    Fsa_new = models.CharField( max_length=50)
    salt_100g = models.CharField(max_length=50)
    salt_g = models.CharField(max_length=50)
    fat_count = models.CharField(max_length=50)
    satfat_count = models.CharField(max_length=50)
    sugar_count = models.CharField(max_length=50)
    salt_count = models.CharField(max_length=50)
    NumberRatings = models.IntegerField()
    class Meta:
        verbose_name = 'HealthyRecipe'
        ordering = ['id']
        db_table = 'HealthyRecipe'
    def __str__(self):
        return self.Name

class UnhealthyRecipe(models.Model):
    id = models.AutoField(primary_key=True)
    URL = models.CharField(max_length=300)
    Name = models.CharField( max_length=500)
    fiber_g = models.CharField( max_length=50)
    sodium_g = models.CharField( max_length=50)
    carbohydrates_g= models.CharField(max_length=50)
    fat_g = models.CharField(max_length=50)
    protein_g = models.CharField(max_length=50)
    sugar_g= models.CharField( max_length=50)
    saturate_g = models.CharField(max_length=50)
    size_g = models.CharField( max_length=50)
    Servings = models.CharField( max_length=50)
    calories_kCal =  models.CharField( max_length=50)
    category = models.CharField( max_length=50)
    image_link = models.CharField( max_length=500)
    fat_100g = models.CharField( max_length=50)
    fiber_100g = models.CharField(max_length=50)
    sugar_100g = models.CharField( max_length=50)
    saturated_100g = models.CharField( max_length=50)
    protien_100g = models.CharField( max_length=50)
    sodium_100mg = models.CharField(max_length=50)
    carbohydrates_100g = models.CharField(max_length=50)
    kj_100g = models.CharField( max_length=50)
    Nutri_score  = models.CharField( max_length=50)
    Fsa_new = models.CharField( max_length=50)
    salt_100g = models.CharField(max_length=50)
    salt_g = models.CharField(max_length=50)
    fat_count = models.CharField(max_length=50)
    satfat_count = models.CharField(max_length=50)
    sugar_count = models.CharField(max_length=50)
    salt_count = models.CharField(max_length=50)
    NumberRatings = models.IntegerField()
    class Meta:
        verbose_name = 'UnhealthyRecipe'
        ordering = ['id']
        db_table = 'UnhealthyRecipe'
    def __str__(self):
        return self.Name






class Healthy_ratings(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey(
        Personal_info,
        blank=False,
        on_delete=models.CASCADE
    )
    healthy_recipe = models.ForeignKey(
        HealthyRecipe,
        # blank=False,
        on_delete=models.CASCADE
    )
    healthy_rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], blank=False, default=0)

    created = models.DateTimeField(auto_now_add=True)
    # session_id = models.CharField(max_length=1000, blank=False, default=None)
    # def __str__(self):
    #     return self.recipe.id
    class Meta:
        unique_together = (('healthy_recipe','person'))
        verbose_name = 'healthy_ratings'
        db_table = 'healthy_ratings'
        
class Unhealthy_ratings(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey(
        Personal_info,
        blank=False,
        on_delete=models.CASCADE
    )
    unhealthy_recipe = models.ForeignKey(
        UnhealthyRecipe,
        # blank=False,
        on_delete=models.CASCADE
    )
    unhealthy_rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], blank=False, default=0)

    created = models.DateTimeField(auto_now_add=True)
    # session_id = models.CharField(max_length=1000, blank=False, default=None)
    class Meta:
        unique_together = (('unhealthy_recipe','person'))
        verbose_name = 'unhealthy_ratings'
        db_table = 'unhealthy_ratings'

# class Recommendations(models.Model):
#     id = models.AutoField(primary_key=True)
#     person = models.ForeignKey("app.Model", 
#         Personal_info,
#         on_delete=models.CASCADE)
#     healthy_recipe    

#     def __str__(self):
#         return 

#     def __unicode__(self):
#         return 


class SelectedRecipe(models.Model):
    id = models.AutoField(primary_key = True)

    person = models.ForeignKey(
        Personal_info,
        blank=False,
        on_delete=models.CASCADE
    )  
    recipe_id = models.IntegerField()  # recipe id that will be saved only
    recipe_name = models.CharField(max_length=200)

    Nutri_score = models.CharField(max_length= 100)
    fsa_score = models.CharField(max_length=100)
    healthiness = models.CharField(max_length=50)

    created = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=1000, blank=False, default=None)
    def __str__(self):
        return self.healthiness
    class Meta:
        unique_together = ('person','recipe_id')
        verbose_name = 'selectedRecipe'
        db_table  ='selectedrecipe'


class EvaluateChoices(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=50,
        editable=False,
        default='EvaluateChoices')

    person = models.ForeignKey(
        Personal_info,
        on_delete=models.CASCADE
    )
    recommend_recipe = models.CharField(max_length=100,
        choices=Recommend_recipe,
        verbose_name='recommend_recipe',
        default=None,
        blank=False
    )
    become_favorite = models.CharField(max_length=100,
        choices=become_favorite,
        verbose_name='become_favorite',
        default=None,
        blank=False
    )
    enjoy_eating = models.CharField(max_length=100,
        choices=enjoy_eating,
        verbose_name='enjoy_eating',
        default=None,
        blank=False
    )
    many_to_choose = models.CharField(max_length=100,
        choices=many_to_Choose,
        verbose_name='many_to_choose',
        default=None,
        blank=False
    )
    easy_choice = models.CharField(max_length=100,
        choices=easy_choice,
        verbose_name='easy_choice',
        default=None,
        blank=False
    )
    choice_overwhelming = models.CharField(max_length=100,
        choices=choice_overwhelming,
        verbose_name='choice_overwhelming',
        default=None,
        blank=False
    )
    created = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=1000, blank=False, default=None)
    class Meta:
        verbose_name = 'EvaluateChoices'
        ordering = ['id']
        db_table = 'EvaluateChoices'

    def __str__(self):
        return "{}".format(self.id)























# class user_rate(models.Model):
#     id = models.AutoField(primary_key=True)
#     person = models.ForeignKey(
#         Personal_info,
#         blank=False,
#         on_delete=models.CASCADE
#     )
#     recipe = models.ForeignKey(
#         Recipes,
#         # blank=False,
#         on_delete=models.CASCADE
#     )

#     recipe_rating = models.IntegerField(
#         validators=[MinValueValidator(0), MaxValueValidator(5)], blank=False, default=0)

#     created = models.DateTimeField(auto_now_add=True)

#     # def __str__(self):
#     #     return self.recipe.id
#     class Meta:
#         unique_together = (('recipe','person'))
#         verbose_name = 'user_rate'
#         db_table = 'user_ratings'
