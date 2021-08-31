from django.contrib import admin
from django.db.models.base import Model
from .models import *
# Register your models here.
import csv
from django.http import HttpResponse

from import_export.admin import ImportExportModelAdmin
from django import forms


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


def export_as_csv_action(description="Export selected objects as CSV file", fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = [field.name for field in opts.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

        # opts = modeladmin.model._meta
        # field_names = set([field.name for field in opts.fields])

        # if fields:
        #     fieldset = set(fields)
        #     field_names = field_names & fieldset

        # elif exclude:
        #     excludeset = set(exclude)
        #     field_names = field_names - excludeset

        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')

        # writer = csv.writer(response)

        # if header:
        #     writer.writerow(list(field_names))
        # for obj in queryset:
        #     writer.writerow([str(getattr(obj, field)).encode("utf-8","replace") for field in field_names])

        # return response

    export_as_csv.short_description = description
    return export_as_csv



# @admin.register(Personal_info)
class Personal_infoAdmin(admin.ModelAdmin):
    list_display = ('id','session_id','created','age','gender','country','education','diet_restriction',
    'diet_goal','cooking_exp','eating_habits')
    actions = [export_as_csv_action("CSV Export")]



# @admin.register(FoodCategory)    
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','person','session_id','category','created')
    actions = [export_as_csv_action("CSV Export")]

# class RecipesAdmin(admin.ModelAdmin):
#     list_display = ('id','URL','Name','category','Size','Serving','Calories',
#     'image_link')
#     actions = [export_as_csv_action("CSV Export")]
# # class user_ratingsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'person','Healthyrecipe','UnhealthyRecipe','recipe_rating','created')

# class user_rateAdmin(admin.ModelAdmin):
#     list_display = ('id', 'person','recipe','recipe_rating','created')


class HealthyRecipeAdmin(ImportExportModelAdmin):
    list_display = ('id','Name','category','Nutri_score','Fsa_new')
    actions = [export_as_csv_action("CSV Export")]
class UnhealthyRecipeAdmin(ImportExportModelAdmin):
    list_display = ('id','Name','category','Nutri_score','Fsa_new')
    actions = [export_as_csv_action("CSV Export")]

class healthy_ratingsAdmin(admin.ModelAdmin):
    list_display = (('id', 'person',
    'healthy_recipe','healthy_rating',
    'created'))
    actions = [export_as_csv_action("CSV Export")]

class unhealthy_ratingsAdmin(admin.ModelAdmin):
    list_display = (('id', 'person',
    'unhealthy_recipe','unhealthy_rating',
    'created'))
    actions = [export_as_csv_action("CSV Export")]
    
class SelectedRecipeAdmin(admin.ModelAdmin):
    list_display = ('id','person','session_id','recipe_name','recipe_id','healthiness','Nutri_score','created')
    actions = [export_as_csv_action("CSV Export")]

class EvaluateChoicesAdmin(admin.ModelAdmin):
    list_display = ('id','person','session_id','recommend_recipe','become_favorite','enjoy_eating',
    'many_to_choose','easy_choice','choice_overwhelming','created')
    actions = [export_as_csv_action("CSV Export")]





admin.site.register(EvaluateChoices, EvaluateChoicesAdmin)
admin.site.register(SelectedRecipe, SelectedRecipeAdmin)
admin.site.register(Healthy_ratings, healthy_ratingsAdmin)
admin.site.register(Unhealthy_ratings, unhealthy_ratingsAdmin)
# admin.site.register(user_rate, user_rateAdmin)
# admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Personal_info, Personal_infoAdmin)
admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(UnhealthyRecipe, UnhealthyRecipeAdmin)
admin.site.register(HealthyRecipe, HealthyRecipeAdmin)



#https://personalizedrecipe2.herokuapp.com/