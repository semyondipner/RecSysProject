""" Recommendation Backend Service """
import random
import numpy as np

import redis
from fastapi import FastAPI

from models import NewItemsEvent, RecommendationsResponse, RecommendationsRequest


app = FastAPI()
redis_con = redis.Redis('localhost')

EPSILON = 0.05
unique_item_ids = set()

@app.get("/healthcheck")
def healthcheck():
    """ 
    /healthcheck возвращает статус сервиса. 
    Для грейдера необходимо, чтобы возвращался код ответа 200 (OK)
    """
    return 200

@app.get('/cleanup')
def cleanup():
    """
    /cleanup производит сброс окружения перед новым запуском грейдера
    (при каждом запуске идентификаторы новые и нужно очистить 
    все возможные кэширования для корректной проверки)
    """
    global unique_item_ids
    unique_item_ids = set()
    try:
        redis_con.delete('*')
        redis_con.json().delete('*')
    except redis.exceptions.ConnectionError:
        pass
    return 200

@app.post('/add_items')
def add_items(request: NewItemsEvent):
    """
    /add_items добавляет в систему новые объекты рекомендации 
    (поле item_ids содержит список идентификаторов объектов, 
    а genres – список списков жанров для соответствующих объектов в item_ids)
    """
    global unique_item_ids
    for item_id in request.item_ids:
        unique_item_ids.add(item_id)
    return 200

@app.get('/recs')
def get_recs(request: RecommendationsRequest):
    """
    /recs/{user_id} возвращает список рекомендаций в виде списка
     объектов для пользователя user_id
    """
    user_id = request.user_id
    global unique_item_ids
    try:
        item_ids = redis_con.json().get('top_items')
    except redis.exceptions.ConnectionError:
        item_ids = None
    if item_ids is None or random.random() < EPSILON:
        item_ids = np.random.choice(list(unique_item_ids), size=20, replace=False).tolist()
    return RecommendationsResponse(item_ids=item_ids)
