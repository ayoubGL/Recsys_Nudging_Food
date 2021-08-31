from datetime import datetime
import csv

from surprise import  SVD
from surprise import Dataset
from surprise import Reader
from collections import defaultdict
import os
import pandas as pd
from .models import Healthy_ratings, Unhealthy_ratings

#--------------------- Append new user to csv file (data) --------------------------
def add_to_csv(person, category):
    hfields = []
    unhfields = []
    
    # get user rating from database
    healthy_rating = Healthy_ratings.objects.filter(person = person)
    unhealthy_rating = Unhealthy_ratings.objects.filter(person = person)
    
    # prepare the fields    
    for field in healthy_rating:
        obj = []
        user_id = str(field.person_id)
        
        # print(user_id,'.............')
        obj.append(str(field.healthy_recipe_id))
        obj.append(user_id)
        obj.append(str(field.healthy_rating))
        
        # obj.append(str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
        hfields.append(obj)
    for field in unhealthy_rating:
        obj = []
        user_id = str(field.person_id)
        
        #print(field.countries_name_id_id,'.............')
        obj.append(str(field.unhealthy_recipe_id))
        obj.append(user_id)
        obj.append(str(field.unhealthy_rating))
        
        # obj.append(str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
        unhfields.append(obj)
    # print('hfiels---------------',hfields)
    # print('unhfiels---------------',unhfields)
    category = category.replace(' ', '_')
    hfile = 'static/rating_matrix/h_'+category+'.csv'
    unhfile = 'static/rating_matrix/unh_'+category+'.csv'
    # print('------', hfile)
    # print('------', unhfile)

    # append new user to csv file
    with open(hfile, 'a') as f:
        for user_obj in hfields:
            writer = csv.writer(f)
            writer.writerow(user_obj)
    with open(unhfile, 'a') as f:
        for user_obj in unhfields:
            writer = csv.writer(f)
            writer.writerow(user_obj)
 
    return 'ok'
    
def get_top_n_for_user(target_user_id, recom_size, categoty):
    
    categoty = categoty.replace(' ', '_')
    hfileCategory = 'static/rating_matrix/h_'+categoty+'.csv'
    unhfileCategory = 'static/rating_matrix/unh_'+categoty+'.csv'

    hfile_path = os.path.expanduser(hfileCategory)
    unhfile_path = os.path.expanduser(unhfileCategory)
    
    reader = Reader(line_format='item user rating', sep=',', rating_scale=(0,5)) #recipeid,userid,rating
    
    hdata = Dataset.load_from_file(hfile_path,reader=reader)
    htrainset = hdata.build_full_trainset()
    htestset = htrainset.build_anti_testset()
    
    unhdata = Dataset.load_from_file(unhfile_path,reader=reader)
    unhtrainset = unhdata.build_full_trainset()
    unhtestset = unhtrainset.build_anti_testset()
    
    

    algo = SVD()
        

    algo.fit(htrainset)
    hpredictions  = algo.test(htestset)

    algo.fit(unhtrainset)
    unhpredictions  = algo.test(unhtestset)

    # First map the predictions to each user.
    htop_n = defaultdict(list)
    for uid, iid, true_r, est, _ in hpredictions:
        htop_n[uid].append((iid, est))

    unhtop_n = defaultdict(list)
    for uid, iid, true_r, est, _ in unhpredictions:
        unhtop_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in htop_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        htop_n[uid] = user_ratings[:recom_size]
    
    for uid, user_ratings in unhtop_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        unhtop_n[uid] = user_ratings[:recom_size]

    return htop_n[str(target_user_id)], unhtop_n[str(target_user_id)]


