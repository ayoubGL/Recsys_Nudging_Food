from django.forms import formset_factory
from django.db.models import Count
import datetime
import pandas as pd
from random import choice, shuffle
from random import randint, shuffle
import random
from sys import prefix
from django import forms
from django.db import reset_queries
from django.forms.models import ModelForm
from django.http import request
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from pandas.core.indexes import category
from .forms import Personal_infoForm, FoodCategory, FoodCategoryForm,Healthy_ratingsForm,Unhealthy_ratingsForm,ChoiceEvaluationForm
# from django.forms import formset_factory, modelformset_factory
from .models import  Personal_info, HealthyRecipe, UnhealthyRecipe,Healthy_ratings,Unhealthy_ratings, SelectedRecipe,EvaluateChoices
from .app import *
import string
import random

def home(request):
    return render(request, 'Labels_Nudges/homes.html', context={})


def personal_info(request):
    if request.method == 'POST':
        personl_info = Personal_infoForm(request.POST)
        # per = Personal_info()
        if personl_info.is_valid():

            answer = personl_info.save(commit=False)
            
            rd_str =''.join(random.choice(string.ascii_lowercase) for _ in range(5))
            time_now = datetime.now().strftime('%H%M%S')
            gene_session = 'dars'+time_now +'_'+str(answer.id)+rd_str
            personl_info.instance.session_id = gene_session

            answer = personl_info.save(commit=True)
            
            request.session['person_id'] = answer.id
            gene_session = 'dars'+time_now +'_'+str(answer.id)+rd_str
            personl_info.instance.session_id = gene_session
            
            request.session['session_id'] = gene_session
            answer = personl_info.save(commit=True)



            return redirect('Labels_Nudges:select_category')
    else:
        personl_info = Personal_infoForm()
    return render(request, 'Labels_Nudges/personal_info.html', context={'form': personl_info})


def select_category(request):
    categoryForm = FoodCategoryForm()
    if request.method == "POST":
        categoryForm = FoodCategoryForm(request.POST)
        # print('============',request)
        if categoryForm.is_valid():
            category = categoryForm.save(commit=False)
            category.person_id = request.session['person_id']
            categoryForm.instance.session_id = request.session['session_id']
            category = categoryForm.save()
            
            return redirect('Labels_Nudges:rate_recipes')
    else:
        return render(request, 'Labels_Nudges/select_category.html', context={'form': categoryForm})
    # else:
    #     return HttpResponse('hello')






def rate_recipes(request):
    user_category = FoodCategory.objects.filter(
        person_id=request.session['person_id']).values_list('category', flat=True)
    user_category = user_category[0]
    print('---category',user_category)
    # extract 5 healthy recipes
    h_recipe = HealthyRecipe.objects.filter(
        category = user_category).values_list('id',flat=True)[0:1]
        
    h_recipe2 = HealthyRecipe.objects.filter(
        category = user_category).values_list('id',flat=True)[1:2]
    h_recipe3 = HealthyRecipe.objects.filter(
        category = user_category).values_list('id',flat=True)[2:3]
    h_recipe4 = HealthyRecipe.objects.filter(
        category = user_category).values_list('id',flat=True)[3:4]
    h_recipe5 = HealthyRecipe.objects.filter(
        category = user_category).values_list('id',flat=True)[4:5]
    # extract 5 unhealthy recipes
    unh_recipe = UnhealthyRecipe.objects.filter(
        category = user_category).values_list('id',flat=True)[0:1]
    unh_recipe2 = UnhealthyRecipe.objects.filter(
        category = user_category).values_list('id',flat=True)[1:2]
    unh_recipe3 = UnhealthyRecipe.objects.filter(
            category = user_category).values_list('id',flat=True)[2:3]
    unh_recipe4 = UnhealthyRecipe.objects.filter(
            category = user_category).values_list('id',flat=True)[3:4]
    unh_recipe5 = UnhealthyRecipe.objects.filter(
        category = user_category).values_list('id',flat=True)[4:5]
    # create forms of healthy and unhealthy recipes
    if request.method == "POST":
        # healthy forms
        h_f_1 = Healthy_ratingsForm(
            request.POST, current_person_category = h_recipe, prefix = 'h_f_1'
        )

        h_f_2 = Healthy_ratingsForm(
            request.POST, current_person_category = h_recipe2, prefix = 'h_f_2'
        )
        h_f_3 = Healthy_ratingsForm(
                    request.POST, current_person_category = h_recipe3, prefix = 'h_f_3'
                )
        h_f_4 = Healthy_ratingsForm(
                    request.POST, current_person_category = h_recipe4, prefix = 'h_f_4'
                )
        h_f_5 = Healthy_ratingsForm(
            request.POST, current_person_category = h_recipe5, prefix = 'h_f_5'
        )

        # unhealthy forms
        unh_f_1 = Unhealthy_ratingsForm(
            request.POST, current_person_category = unh_recipe, prefix = 'unh_f_1'
        )
        unh_f_2= Unhealthy_ratingsForm(
            request.POST, current_person_category = unh_recipe2, prefix = 'unh_f_2'
        )

        unh_f_3 = Unhealthy_ratingsForm(
            request.POST, current_person_category = unh_recipe3, prefix = 'unh_f_3'
        )

        unh_f_4 = Unhealthy_ratingsForm(
            request.POST, current_person_category = unh_recipe4, prefix = 'unh_f_4'
        )

        unh_f_5 = Unhealthy_ratingsForm(
            request.POST, current_person_category = unh_recipe5, prefix = 'unh_f_5'
        )
        # five healthy instances
        h_rating1 = Healthy_ratings()
        h_rating2 = Healthy_ratings()
        h_rating3 = Healthy_ratings()
        h_rating4 = Healthy_ratings()
        h_rating5 = Healthy_ratings()

        unh_rating1 = Unhealthy_ratings()
        unh_rating2 = Unhealthy_ratings()
        unh_rating3 = Unhealthy_ratings()
        unh_rating4 = Unhealthy_ratings()
        unh_rating5 = Unhealthy_ratings()

        # valid healthy and unhltheay forms
        if h_f_1.is_valid() and h_f_2.is_valid() and h_f_3.is_valid() and h_f_4.is_valid() and h_f_5.is_valid() and unh_f_1.is_valid() and unh_f_2.is_valid() and unh_f_3.is_valid() and unh_f_4.is_valid() and unh_f_5.is_valid() :
            person = Personal_info.objects.get(
                id=request.session['person_id'])

                # healthy forms
        # ----------------------------------- h_f_1/ unh_f_1--------------------------
            healthy_recipe_id = h_f_1.cleaned_data.get('healthy_recipe')
            user_healthy_ratings =h_f_1.cleaned_data.get('healthy_rating')
            h_rating1.healthy_recipe = healthy_recipe_id
            h_rating1.healthy_rating = user_healthy_ratings
            

            unhealthy_recipe_id = unh_f_1.cleaned_data.get('unhealthy_recipe')
            user_unhealthy_ratings = unh_f_1.cleaned_data.get('unhealthy_rating')
            unh_rating1.unhealthy_recipe = unhealthy_recipe_id
            unh_rating1.unhealthy_rating = user_unhealthy_ratings

            h_rating1.person = person
            unh_rating1.person = person
            h_rating1.save() 
            unh_rating1.save()     

    # ----------------------------------- h_f_2/ unh_f_2--------------------------
            healthy_recipe_id = h_f_2.cleaned_data.get('healthy_recipe')
            user_healthy_ratings =h_f_2.cleaned_data.get('healthy_rating')
            h_rating2.healthy_recipe = healthy_recipe_id
            h_rating2.healthy_rating = user_healthy_ratings
            

            unhealthy_recipe_id = unh_f_2.cleaned_data.get('unhealthy_recipe')
            user_unhealthy_ratings = unh_f_2.cleaned_data.get('unhealthy_rating')
            unh_rating2.unhealthy_recipe = unhealthy_recipe_id
            unh_rating2.unhealthy_rating = user_unhealthy_ratings

            h_rating2.person = person
            unh_rating2.person = person
            h_rating2.save() 
            unh_rating2.save()   
    # ----------------------------------- h_f_3/ unh_f_3--------------------------
            healthy_recipe_id = h_f_3.cleaned_data.get('healthy_recipe')
            user_healthy_ratings =h_f_3.cleaned_data.get('healthy_rating')
            h_rating3.healthy_recipe = healthy_recipe_id
            h_rating3.healthy_rating = user_healthy_ratings
            

            unhealthy_recipe_id = unh_f_3.cleaned_data.get('unhealthy_recipe')
            user_unhealthy_ratings = unh_f_3.cleaned_data.get('unhealthy_rating')
            unh_rating3.unhealthy_recipe = unhealthy_recipe_id
            unh_rating3.unhealthy_rating = user_unhealthy_ratings

            h_rating3.person = person
            unh_rating3.person = person
            h_rating3.save() 
            unh_rating3.save()        

    # ----------------------------------- h_f_4/ unh_f_4--------------------------
            healthy_recipe_id = h_f_4.cleaned_data.get('healthy_recipe')
            user_healthy_ratings =h_f_4.cleaned_data.get('healthy_rating')
            h_rating4.healthy_recipe = healthy_recipe_id
            h_rating4.healthy_rating = user_healthy_ratings
            

            unhealthy_recipe_id = unh_f_4.cleaned_data.get('unhealthy_recipe')
            user_unhealthy_ratings = unh_f_4.cleaned_data.get('unhealthy_rating')
            unh_rating4.unhealthy_recipe = unhealthy_recipe_id
            unh_rating4.unhealthy_rating = user_unhealthy_ratings

            h_rating4.person = person
            unh_rating4.person = person
            h_rating4.save() 
            unh_rating4.save()   

    # ----------------------------------- h_f_5/ unh_f_5--------------------------
            healthy_recipe_id = h_f_5.cleaned_data.get('healthy_recipe')
            user_healthy_ratings =h_f_5.cleaned_data.get('healthy_rating')
            h_rating5.healthy_recipe = healthy_recipe_id
            h_rating5.healthy_rating = user_healthy_ratings
            

            unhealthy_recipe_id = unh_f_5.cleaned_data.get('unhealthy_recipe')
            user_unhealthy_ratings = unh_f_5.cleaned_data.get('unhealthy_rating')
            unh_rating5.unhealthy_recipe = unhealthy_recipe_id
            unh_rating5.unhealthy_rating = user_unhealthy_ratings

            h_rating5.person = person
            unh_rating5.person = person
            h_rating5.save() 
            unh_rating5.save()   

            return redirect("Labels_Nudges:recipe_recommendations")
    else:
                    # healthy forms
        h_f_1 = Healthy_ratingsForm(
            current_person_category = h_recipe, prefix = 'h_f_1'
        )

        h_f_2 = Healthy_ratingsForm(
            current_person_category = h_recipe2, prefix = 'h_f_2'
        )
        h_f_3 = Healthy_ratingsForm(
                    current_person_category = h_recipe3, prefix = 'h_f_3'
                )
        h_f_4 = Healthy_ratingsForm(
                    current_person_category = h_recipe4, prefix = 'h_f_4'
                )
        h_f_5 = Healthy_ratingsForm(
            current_person_category = h_recipe5, prefix = 'h_f_5'
        )

        # unhealthy forms
        unh_f_1 = Unhealthy_ratingsForm(
            current_person_category = unh_recipe, prefix = 'unh_f_1'
        )
        unh_f_2= Unhealthy_ratingsForm(
            current_person_category = unh_recipe2, prefix = 'unh_f_2'
        )

        unh_f_3 = Unhealthy_ratingsForm(
            current_person_category = unh_recipe3, prefix = 'unh_f_3'
        )

        unh_f_4 = Unhealthy_ratingsForm(
            current_person_category = unh_recipe4, prefix = 'unh_f_4'
        )

        unh_f_5 = Unhealthy_ratingsForm(
            current_person_category = unh_recipe5, prefix = 'unh_f_5'
        )
    return render(request, 'Labels_Nudges/rate_h_unh.html', context={
                'h_f_1': h_f_1, 'unh_f_1':unh_f_1, 
                'h_f_2': h_f_2, 'unh_f_2':unh_f_2,
                'h_f_3': h_f_3, 'unh_f_3':unh_f_3, 
                'h_f_4': h_f_4, 'unh_f_4':unh_f_4, 
                'h_f_5': h_f_5, 'unh_f_5':unh_f_5
                
                })





def recipe_recommendations(request):

    # add rating of current user to rating matrix
    person = request.session['person_id']
    user_category = FoodCategory.objects.filter(
        person_id=request.session['person_id']).values_list('category', flat=True)
    user_category = user_category[0]
    target_user = add_to_csv(person, category=user_category)
    unh_recipe5 = UnhealthyRecipe.objects.filter(
        category = user_category).values_list('id',flat=True)[4:5]

    # print('add-----------', target_user)
    # print('category----------', user_category)

    # get recommendation
    recom_size = 5
    htop_n_for_target_user = []
    unhtop_n_for_target_user = []
    htop_n_for_target_user,unhtop_n_for_target_user = get_top_n_for_user(person,recom_size, user_category)
    
    # print('-----------HT',htop_n_for_target_user)
    # print('-----------Unht',unhtop_n_for_target_user)

    # get recipe info and send them to tmeplate
    id_h_recipes = [] 
    # for i in htop_n_for_target_user:
    #     id_h_recipes.append(i[0])
    [id_h_recipes.append(i[0]) for i in htop_n_for_target_user]

    id_unh_recipes = []
    [id_unh_recipes.append(i[0]) for i in unhtop_n_for_target_user]
    # for i in unhtop_n_for_target_user:
    #     id_unh_recipes.append(i[0])

    # print(f'-------healthy_ids: {id_h_recipes}')
    # print(f'--------unhealthy_ids: {id_unh_recipes}')
    
    # extract 5 healthy recipes
    h_0_recipe = HealthyRecipe.objects.get(id=id_h_recipes[0])
    h_1_recipe = HealthyRecipe.objects.get(id=id_h_recipes[1])
    h_2_recipe = HealthyRecipe.objects.get(id=id_h_recipes[2])
    h_3_recipe = HealthyRecipe.objects.get(id=id_h_recipes[3])
    h_4_recipe = HealthyRecipe.objects.get(id=id_h_recipes[4])
    # extract 5 unhhealthy recipes
    unh_0_recipe = UnhealthyRecipe.objects.get(id=id_unh_recipes[0])
    unh_1_recipe = UnhealthyRecipe.objects.get(id=id_unh_recipes[1])
    unh_2_recipe = UnhealthyRecipe.objects.get(id=id_unh_recipes[2])
    unh_3_recipe = UnhealthyRecipe.objects.get(id=id_unh_recipes[3])
    unh_4_recipe = UnhealthyRecipe.objects.get(id=id_unh_recipes[4])
    
    # selected recipe model
    selected_recipe = SelectedRecipe() 

    # initialise healthy forms with extracted data
    if request.method == "POST":

        # if the user already select a recipe
        person = request.session['person_id']
        user_selected = SelectedRecipe.objects.filter(person_id = person)
        if user_selected:
            SelectedRecipe.objects.filter(person_id=person).delete()

        # print('Request POST------------',request.POST)
        recipe_name = request.POST.get('recipe_name')
        recipe_id = request.POST.get('recipe_id')
        recipe_h  = request.POST.get('healthiness')

        if recipe_h == 'healthy':
            nutri__fsa = HealthyRecipe.objects.filter(id=recipe_id).values_list('Nutri_score', 'Fsa_new',)
        else:
            nutri__fsa = UnhealthyRecipe.objects.filter(id=recipe_id).values_list('Nutri_score', 'Fsa_new')
        selected_recipe.Nutri_score = nutri__fsa[0][0]
        selected_recipe.fsa_score = nutri__fsa[0][1]
        selected_recipe.person_id= person
        selected_recipe.recipe_name = recipe_name
        selected_recipe.recipe_id = recipe_id
        selected_recipe.healthiness = recipe_h
        selected_recipe.session_id = request.session['session_id']
        selected_recipe.save()


        return redirect('Labels_Nudges:choice_evaluation')
    else:
        Serving_size = float(h_0_recipe.size_g) // float(h_0_recipe.Servings)
        
        h_0 = [h_0_recipe.Name, id_h_recipes[0], 'healthy', h_0_recipe.image_link, int(float(h_0_recipe.calories_kCal)), int(float(h_0_recipe.Servings)),int(float(Serving_size)), h_0_recipe.Nutri_score]
        h_1 = [h_1_recipe.Name, id_h_recipes[1], 'healthy', h_1_recipe.image_link, int(float(h_1_recipe.calories_kCal)), int(float(h_1_recipe.Servings)),int(float(Serving_size)), h_1_recipe.Nutri_score]
        h_2 = [h_2_recipe.Name, id_h_recipes[2], 'healthy', h_2_recipe.image_link, int(float(h_2_recipe.calories_kCal)), int(float(h_2_recipe.Servings)),int(float(Serving_size)), h_2_recipe.Nutri_score]
        h_3 = [h_3_recipe.Name, id_h_recipes[3], 'healthy', h_3_recipe.image_link, int(float(h_3_recipe.calories_kCal)), int(float(h_3_recipe.Servings)),int(float(Serving_size)), h_3_recipe.Nutri_score]
        h_4 = [h_4_recipe.Name, id_h_recipes[4], 'healthy', h_4_recipe.image_link, int(float(h_4_recipe.calories_kCal)), int(float(h_4_recipe.Servings)),int(float(Serving_size)), h_4_recipe.Nutri_score]
        print("Nutri_score",h_0[7],'Image',h_0[3] )


        unh_0 = [unh_0_recipe.Name, id_unh_recipes[0], 'unhealthy', unh_0_recipe.image_link, int(float(unh_0_recipe.calories_kCal)), int(float(unh_0_recipe.Servings)),int(float(Serving_size)), unh_0_recipe.Nutri_score]
        unh_1 = [unh_1_recipe.Name, id_unh_recipes[1], 'unhealthy', unh_1_recipe.image_link, int(float(unh_1_recipe.calories_kCal)), int(float(unh_1_recipe.Servings)),int(float(Serving_size)), unh_1_recipe.Nutri_score]
        unh_2 = [unh_2_recipe.Name, id_unh_recipes[2], 'unhealthy', unh_2_recipe.image_link, int(float(unh_2_recipe.calories_kCal)), int(float(unh_2_recipe.Servings)),int(float(Serving_size)), unh_2_recipe.Nutri_score]
        unh_3 = [unh_3_recipe.Name, id_unh_recipes[3], 'unhealthy', unh_3_recipe.image_link, int(float(unh_3_recipe.calories_kCal)), int(float(unh_3_recipe.Servings)),int(float(Serving_size)), unh_3_recipe.Nutri_score]
        unh_4 = [unh_4_recipe.Name, id_unh_recipes[4], 'unhealthy', unh_4_recipe.image_link, int(float(unh_4_recipe.calories_kCal)), int(float(unh_4_recipe.Servings)),int(float(Serving_size)), unh_4_recipe.Nutri_score]

    # send forms
    return render(request,'Labels_Nudges/recipe_recommendations.html',context={'h_':htop_n_for_target_user, 
                                                'unh_':unhtop_n_for_target_user,
                                                'h_0':h_0,
                                                'h_1':h_1,
                                                'h_2':h_2,
                                                'h_3':h_3,
                                                'h_4':h_4,
                                                'unh_0':unh_0,
                                                'unh_1':unh_1,
                                                'unh_2':unh_2,
                                                'unh_3':unh_3,
                                                'unh_4':unh_4,
                                                })



def choice_evaluation(request):
    if request.method == 'POST':
        evaluation_form = ChoiceEvaluationForm(request.POST)
        person = request.session['person_id']
        ChoiceEvaltion = EvaluateChoices()
        if evaluation_form.is_valid():
            # print("-----------here we are")
            # ChoiceEvaltion.person = request.session['person_id']
            evaluation_ = evaluation_form.save(commit=False)
            evaluation_.person_id = person
            evaluation_.session_id = request.session['session_id']
            evaluation_.save()
            return redirect('Labels_Nudges:thank_u')
    else:
         evaluation_form = ChoiceEvaluationForm()
    return render(request, 'Labels_Nudges/choice_evaluation.html', context={'eval_form': evaluation_form})
    

def thank_u(request):

    return render(request, 'Labels_Nudges/thanks.html', context={'session_id':request.session['session_id']})






def error_404(request,exception):
    data = {}
    return render(request, 'Labels_Nudges/404.html',data)
def error_500(request):
        data = {}
        return render(request,'Labels_Nudges/404.html', data)







































# def rate_items(request):
#     # name of cateogry that user selected
#     user_category = FoodCategory.objects.filter(
#         person_id=request.session['person_id']).values_list('category', flat=True)
#     user_category = user_category[0]

#     # recipes of category for a user

#     category_recipes = Recipes.objects.filter(
#         category=user_category).values_list('id', flat=True)[0:1]
    
#     # category_recipes11 = Recipes.objects.filter(
#     #     category=user_category).values_list('id', flat=True)[10:11]


# # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4

#     # category_recipes = CategoryRecipes(user_category)
#     # category_recipes2 = CategoryRecipes(user_category)

#     if request.method == "POST":

#         f_1 = user_rateForm(
#             request.POST, prefix='f_1')


#         user_rating1 = user_rate()

#         # user_rating11 = user_rating()
#         # print('form error==========', form.errors)
#         if f_1.is_valid() :
#             # print('------valid')
#             # user_rating.save(commit = False)
#             # print('------',recipe_id)
#             person = Personal_info.objects.get(
#                 id=request.session['person_id'])

# ----------------------------------- f_1--------------------------
    #         recipe_id = f_1.cleaned_data.get('recipe')
    #         user_ratings = f_1.cleaned_data.get('recipe_rating')
            

    #         user_rating1.recipe = recipe_id
    #         user_rating1.person = person
    #         user_rating1.recipe_rating = user_ratings
    #         user_rating1.save()

    #         return redirect('Labels_Nudges:recipe_recommendations')
    # else:
    #     recipe_ = Recipes.objects.filter(category = user_category)
    #     f_1 = user_rateForm(
    #             initial={'recipe':recipe_}
    #          , prefix='f_1')

       

    #     # recipesFormset = modelformset_factory(user_rating,form = user_ratingForm, extra = 5,max_num=40)
    # return render(request, 'Labels_Nudges/rate_items.html', context={'f_1': f_1})
    
