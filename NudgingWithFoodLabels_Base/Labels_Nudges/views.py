from django.forms import formset_factory
from django.db.models import Count
import datetime
import pandas as pd
from random import choice, randint, shuffle, sample
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
from pkg_resources import require
from .forms import Personal_infoForm, FoodCategory, FoodCategoryForm,Healthy_ratingsForm,Unhealthy_ratingsForm,ChoiceEvaluationForm
# from django.forms import formset_factory, modelformset_factory
from .models import Personal_info, HealthyRecipe, UnhealthyRecipe,Healthy_ratings,Unhealthy_ratings, SelectedRecipe,EvaluateChoices
from .app import *
import string
from datetime import datetime


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


            request.session['rcp'] = []
            return redirect('Labels_Nudges:select_category')
    else:
        personl_info = Personal_infoForm()
    return render(request, 'Labels_Nudges/personal_info.html', context={'form': personl_info})

def random_recipes(category):
    size = len(HealthyRecipe.objects.filter(category = category))
    ten_pr = size // 10
    if ten_pr < 5:
        ten_pr = size // 2
    h_recipes = HealthyRecipe.objects.filter(category = category).order_by('-NumberRatings').values_list('id', flat=True)[:ten_pr]
    # print(f'len ------------------------- {len(h_recipes)} {size}')
    # unh_recipes = UnhealthyRecipe.objects.filter(category = category).order_by('-NumberRatings').values_list('id', flat=True)[:ten_pr]
    h_5 = sample(list(h_recipes), 5)
    return h_5


def select_category(request):
    categoryForm = FoodCategoryForm()
    if request.method == "POST":
        categoryForm = FoodCategoryForm(request.POST)
        if categoryForm.is_valid():
            category = categoryForm.save(commit=False)
            category.person_id = request.session['person_id']
            categoryForm.instance.session_id = request.session['session_id']
            category = categoryForm.save()

            user_category = FoodCategory.objects.filter(
            person_id=request.session['person_id']).values_list('category', flat=True)
            user_category = user_category[0]
            # print('categoruy=====', user_category)
            recipes = random_recipes(user_category)
            # rcp = []
            # for i in recipes[:2]:
            #     rcp.append(HealthyRecipe.objects.filter(id=i).values_list('id'))
            # request.session['rcp'] = list(rcp)
            # print('session------',request.session['rcp'])
            request.session['rcp'] = recipes[:2]
            return redirect('Labels_Nudges:rate_recipes')
    else:
        categoryForm = FoodCategoryForm()
    return render(request, 'Labels_Nudges/select_category.html', context={'form': categoryForm})





def rate_recipes(request):
    # user_category = FoodCategory.objects.filter(
    #     person_id=request.session['person_id']).values_list('category', flat=True)
    # user_category = user_category[0]
    # print('---category',user_category)
    #------- random top 10 recipes based on number of ratings -----------
    
    #-------------------------------------------------------------------
    
    rcp = []    
    print('session------',request.session['rcp'])
    # if not request.session['rcp']:
    #     print('again---t')
    for i in request.session['rcp']:
        rcp.append(HealthyRecipe.objects.filter(id=i))
    
    
    if request.method == "POST":
            # healthy forms
            # rcp = request.session['rcp']
            h_f_1 = Healthy_ratingsForm(request.POST, prefix = 'h_f_1')
            h_f_2 = Healthy_ratingsForm(request.POST,prefix = 'h_f_2')
            
            # five healthy instances
            h_rating1 = Healthy_ratings()
            h_rating2 = Healthy_ratings()
            # valid healthy and unhltheay forms
            if h_f_1.is_valid() and h_f_2.is_valid() :
                person = Personal_info.objects.get(id=request.session['person_id'])
                h_rating1.person = person
                h_rating1.healthy_recipe_id = rcp[0][0].id
                h_rating1.healthy_rating = h_f_1.cleaned_data.get('healthy_rating')
                h_rating1.save()
                
                h_rating2.person = person
                h_rating2.healthy_recipe_id = rcp[1][0].id
                h_rating2.healthy_rating = h_f_2.cleaned_data.get('healthy_rating')
                h_rating2.save()
                print('recipes-----, saved',rcp[0][0].Name,'---', rcp[1][0].Name)    
                return HttpResponse([rcp[0][0].Name, rcp[1][0].Name])
    else:           
            h_f_1 = Healthy_ratingsForm(prefix = 'h_f_1')
            h_f_2 = Healthy_ratingsForm(prefix = 'h_f_2')
            # rcp = request.session['rcp']
            print(rcp[0][0].Name,'---',rcp[1][0].Name)         
    return render(request, 'Labels_Nudges/rate_h_unh.html', context={
                        'h_f_1': h_f_1, 'hf_d1':rcp[0],
                        'h_f_2':h_f_2, 'hf_d2': rcp[1],
                        # 'h_f_2': h_f_2, 'unh_f_2':unh_f_2,
                        # 'h_f_3': h_f_3, 'unh_f_3':unh_f_3, 
                        # 'h_f_4': h_f_4, 'unh_f_4':unh_f_4, 
                        # 'h_f_5': h_f_5, 'unh_f_5':unh_f_5
                        
                        })
    




def recipe_recommendations(request):

    # add rating of current user to rating matrix
    person = request.session['person_id']
    user_category = FoodCategory.objects.filter(
        person_id=request.session['person_id']).values_list('category', flat=True)
    user_category = user_category[0]
    target_user = add_to_csv(person, category=user_category)
    # unh_recipe5 = UnhealthyRecipe.objects.filter(
    #     category = user_category).values_list('id',flat=True)[4:5]

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
        Serving_size1 = float(h_1_recipe.size_g) // float(h_1_recipe.Servings)
        Serving_size2 = float(h_2_recipe.size_g) // float(h_2_recipe.Servings)
        Serving_size3 = float(h_3_recipe.size_g) // float(h_3_recipe.Servings)
        Serving_size4 = float(h_4_recipe.size_g) // float(h_4_recipe.Servings)
        
        h_0 = [h_0_recipe.Name, id_h_recipes[0], 'healthy', h_0_recipe.image_link, int(float(h_0_recipe.calories_kCal)), int(float(h_0_recipe.Servings)),int(float(Serving_size))]
        h_1 = [h_1_recipe.Name, id_h_recipes[1], 'healthy', h_1_recipe.image_link, int(float(h_1_recipe.calories_kCal)), int(float(h_1_recipe.Servings)),int(float(Serving_size1))]
        h_2 = [h_2_recipe.Name, id_h_recipes[2], 'healthy', h_2_recipe.image_link, int(float(h_2_recipe.calories_kCal)), int(float(h_2_recipe.Servings)),int(float(Serving_size2))]
        h_3 = [h_3_recipe.Name, id_h_recipes[3], 'healthy', h_3_recipe.image_link, int(float(h_3_recipe.calories_kCal)), int(float(h_3_recipe.Servings)),int(float(Serving_size3))]
        h_4 = [h_4_recipe.Name, id_h_recipes[4], 'healthy', h_4_recipe.image_link, int(float(h_4_recipe.calories_kCal)), int(float(h_4_recipe.Servings)),int(float(Serving_size4))]
        
        Serving_size_ = float(unh_0_recipe.size_g) // float(unh_0_recipe.Servings)
        Serving_size_1 = float(unh_1_recipe.size_g) // float(unh_1_recipe.Servings)
        Serving_size_2 = float(unh_2_recipe.size_g) // float(unh_2_recipe.Servings)
        Serving_size_3 = float(unh_3_recipe.size_g) // float(unh_3_recipe.Servings)
        Serving_size_4 = float(unh_4_recipe.size_g) // float(unh_4_recipe.Servings)

        unh_0 = [unh_0_recipe.Name, id_unh_recipes[0], 'unhealthy', unh_0_recipe.image_link, int(float(unh_0_recipe.calories_kCal)), int(float(unh_0_recipe.Servings)),int(float(Serving_size_))]
        unh_1 = [unh_1_recipe.Name, id_unh_recipes[1], 'unhealthy', unh_1_recipe.image_link, int(float(unh_1_recipe.calories_kCal)), int(float(unh_1_recipe.Servings)),int(float(Serving_size_1))]
        unh_2 = [unh_2_recipe.Name, id_unh_recipes[2], 'unhealthy', unh_2_recipe.image_link, int(float(unh_2_recipe.calories_kCal)), int(float(unh_2_recipe.Servings)),int(float(Serving_size_2))]
        unh_3 = [unh_3_recipe.Name, id_unh_recipes[3], 'unhealthy', unh_3_recipe.image_link, int(float(unh_3_recipe.calories_kCal)), int(float(unh_3_recipe.Servings)),int(float(Serving_size_3))]
        unh_4 = [unh_4_recipe.Name, id_unh_recipes[4], 'unhealthy', unh_4_recipe.image_link, int(float(unh_4_recipe.calories_kCal)), int(float(unh_4_recipe.Servings)),int(float(Serving_size_4))]

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
            # ChoiceEvaltion.person_id = evaluation_form.foriengkey
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
    
