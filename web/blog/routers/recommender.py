from typing import List, Optional
from fastapi import APIRouter, Depends, status,Response, HTTPException
from blog import schemas, models, database 
from sqlalchemy.orm import Session

import pandas as pd
import torch
import torch.nn as nn
from blog.repository import recommender_func
from blog.article_recommendation import test_utils 
from ..article_recommendation.model import NMF


router = APIRouter(
    prefix = "/recommendation",
     tags=['Recommendation']
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using: ",device)
data_path = '/home/ravi/fastapi/fastapi/app/web/blog/article_recommendation/train.csv'
le_url_mapping,le_user_mapping, user_le_mapping, url_to_keyword_label, user_emb_sizes, url_emb_sizes = test_utils.load_data(data_path)

# url_list = url_list =  [le_url_mapping[i] for i in range(len(le_url_mapping))]
url_generator = recommender_func.url_generator()
all_url_df =  url_generator.get_url_by_time_only('52_weeks')
all_url_list = all_url_df['url'].unique()

dropout = 0.01
learning_rate = 0.001

model_name = '/home/ravi/fastapi/fastapi/app/web/blog/article_recommendation/NCF_checkpoint_CPU_updated.pth.tar'
model = NMF(user_emb_sizes = user_emb_sizes, url_emb_sizes = url_emb_sizes, dropout = dropout).to(device)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr= learning_rate)


print("loading Model.....")
test_utils.load_checkpoint(torch.load(model_name), model, optimizer)
model.train() 
print("Finish Loading Model")


# @router.get('/', response_model = List[schemas.recommender])
# def all(db: Session = Depends(database.get_db)):
#     return recommender_func.show_user_name(db)

@router.get('/{id}', status_code = 200)
def get_user(id):
    print(id,int(id),type(id))
    return {"user: " : le_user_mapping[int(id)]}


@router.get('/get_urls/{id}', status_code = 200)
def get_recommendation(id):
    user = le_user_mapping[int(id)]
    return recommender_func.get_urls(user,all_url_list, model,user_le_mapping, url_to_keyword_label)


@router.get('/get_urls_of/{user_id}', status_code = 200)
def get_recommendation(user_id: int, site: Optional[str] = None, time: Optional[str] =  None):
    user = le_user_mapping[int(user_id)]
    
    if site and time :
        url_df = url_generator.get_url_by_time_and_site(site,time)
    elif site:        
        url_df =  url_generator.get_df_by_site(site)
    elif time:        
        url_df =  url_generator.get_url_by_time_only(time)
    else:
        url_df =  url_generator.get_url_by_time_only('1_weeks')

    url_list = url_df['url'].unique()

    return recommender_func.get_urls(user,url_list, model,user_le_mapping, url_to_keyword_label)