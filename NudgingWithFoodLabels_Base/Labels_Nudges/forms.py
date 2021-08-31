from django import forms
from django.core.exceptions import ValidationError
from django.db import close_old_connections, models
from django.db.models import fields
from django.forms import widgets
from .models import FoodCategory, HealthyRecipe, Personal_info, UnhealthyRecipe, Healthy_ratings,Unhealthy_ratings,EvaluateChoices
from django_starfield import Stars
from django.forms import formset_factory, modelformset_factory


class Personal_infoForm(forms.ModelForm):
    class Meta:
        model = Personal_info
        exclude = ('id', 'created', 'title','session_id')
        widgets = {
            'gender': forms.RadioSelect(attrs={'label_suffix': '', 'required': True}),
            'age': forms.Select(attrs={'class': 'form-select form-select-sm clabel'}),
            'country': forms.Select(attrs={'class': 'form-select form-select-sm clabel', 'required': True}),
            'education': forms.Select(attrs={'class': 'form-select form-select-sm clabel'}),
            'cooking_exp': forms.RadioSelect(attrs={'label_suffix': '', }),
            'eating_habits': forms.RadioSelect(attrs={'label_suffix': '', }),
        }
        labels = {
            'gender': 'Gender',
            'age': 'Age',
            'Country': 'Nationality',
            'education': 'Your highest completed education',
            'diet_restriction': 'Indicate any dietary restrictions or health conditions',
            'diet_goal': 'Do you have any eating goals',
            'cooking_exp': 'I consider my cooking experience to be',
            'eating_habits': 'I consider my eating habits to be',
        }


class FoodCategoryForm(forms.ModelForm):

    class Meta:
        model = FoodCategory
        exclude = ('id', 'created', 'person','session_id')
        widgets = {
            'category': forms.Select(attrs={'class': 'btn'})}
        labels = {
            'category': 'Food Category'
        }



class Healthy_ratingsForm(forms.ModelForm):
    healthy_rating = forms.IntegerField(required= True, widget=Stars(), error_messages={'required':'Please rate this recipe'}, label='')
    class Meta:
        model=Healthy_ratings
        exclude=('id', 'person', 'created','session_id','healthy_recipe')


class Unhealthy_ratingsForm(forms.ModelForm):
    unhealthy_recipe = forms.ModelChoiceField(queryset=None, required=True, widget=forms.RadioSelect())
    unhealthy_rating = forms.IntegerField(required= True, widget=Stars())
    

    def __init__(self, *args, **kwargs):
        current_person_category = kwargs.pop('current_person_category')
        super(Unhealthy_ratingsForm, self).__init__(*args, **kwargs)

        self.fields['unhealthy_recipe'].queryset = UnhealthyRecipe.objects.filter(
            id = current_person_category
        )

        self.fields['unhealthy_recipe']
        self.fields['unhealthy_recipe'].label = False
        self.fields['unhealthy_rating'].label = False
        self.fields['unhealthy_rating'].required = True
        self.fields['unhealthy_rating'].error_messages['required'] = 'Please rate this recipe'
        self.fields['unhealthy_recipe'].empty_label = None  # remove the empty label

    class Meta:
        model=Unhealthy_ratings
        exclude=('id', 'person', 'created','session_id')




class ChoiceEvaluationForm(forms.ModelForm):
    class Meta:
        model = EvaluateChoices
        exclude = ('id', 'created', 'title','person','session_id')
        widgets = {
            'recommend_recipe': forms.RadioSelect(attrs={'label_suffix': '', 'required': True}), # label_suffix to remove : after attributes
            'become_favorite': forms.RadioSelect(attrs={'label_suffix': '', 'required': True}),
            'enjoy_eating': forms.RadioSelect(attrs={'label_suffix': '', 'required': True}),
            'many_to_choose': forms.RadioSelect(attrs={'label_suffix': '', 'required': True}),
            'easy_choice': forms.RadioSelect(attrs={'label_suffix': '', 'required': True}),
            'choice_overwhelming': forms.RadioSelect(attrs={'label_suffix': '', 'required': True}),
        }
        labels = {
            'recommend_recipe': 'I would recommend the chosen recipe to others ',
            'become_favorite': 'My chosen recipe could become one of my favorites ',
            'enjoy_eating': 'I think I would enjoy the chosen recipe ',
            'many_to_choose': 'I changed my mind several times before making a decision ',
            'diet_restriction': 'Do you have any dietary restrictions',
            'easy_choice': 'It was easy to make this choice ',
            'choice_overwhelming': 'Making a choice was overwhelming ',
        }





# class SelectedRecipeForm(forms.ModelForm):
#     # choices = [('1','test')]
#     # recipe_name = forms.ChoiceField(choices=choices,required=True, widget = forms.RadioSelect())
#     class Meta:
#         model = SelectedRecipe
#         exclude = ('id','person','recipe_id','created')
#         # widgets = {
#         #     "recipe_name": forms.RadioSelect(),
#         #     "healthiness":forms.TextInput()
#         # }
#         # labels = {
#         #     'recipe_id': None,
#         #     'healthness':None
#         # }
    













# class user_rateForm(forms.ModelForm):
#     recipe_rating = forms.IntegerField(required=True, widget=Stars())
#     # recipe = forms.CharField(max_length=50, required=False)
#     # person = forms.IntegerField(required=True)
#     # recipe = forms.ModelChoiceField(queryset=Recipes.objects.all(), empty_label=None, widget= forms.RadioSelect(), initial=0, to_field_name='id')


#     class Meta:
#         model=user_rate
#         exclude=('id', 'person', 'created')

# # recipesFormset = formset_factory(form = user_ratingsForm, extra = 5,max_num=40)
# # recipesFormset = modelformset_factory(user_ratings,form = user_ratingsForm, extra = 5,max_num=40)



