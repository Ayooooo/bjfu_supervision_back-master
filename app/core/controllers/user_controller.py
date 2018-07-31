from app.core.models import User,Event
from flask_pymongo import ObjectId
import json
from app.core.controllers.common_controller import dict_serializable

def find_user(mongo, condition=None):
    if condition is None:
        return mongo.db.user.find()
    if '_id' in condition:
         condition['_id']['$in'] = [ObjectId(item) for item in condition['_id']['$in']]
    datas = mongo.db.user.find(condition)
    return datas


def insert_user(mongo, user):
    user.items_to_dict()
    mongo.db.user.insert(user.model)


def delete_user(mongo, condition=None):
    if condition is None:
        return False
    try:
        mongo.db.user.update(condition, {"$set":{"using":False}})
    except:
        return False
    return True


def request_to_class(json_request):
    user = User()
    name = json_request.get('name', None)
    information_datas = json_request.get('information', {})
    events_datas = json_request.get('events',[])
    user.name = name
    if information_datas is not None:
        for k, v in information_datas.items():
            if k in user.model['information']:
                user.model['information'][k] = v
    if events_datas is not None:
        for events_data in events_datas:
            event = Event()
            for k, v in events_data.items():
                if k in event.model:
                    event.model[k] = v
            user.events.append(event)
    return user

def update_user(mongo, condition=None, change_items = None):
    if condition is None:
        return False
    try:
        mongo.db.user.update(condition, {"$set":change_items})
    except:
        return False
    return True

def to_json_list(user):
    _id = user.get('_id', None)
    name = user.get('name', None)
    information = user.get('information', {})
    events=user.get('events',[])
    using = user.get('using', None)
    json_list = {
        '_id': _id,
        'name ': name,
        'information': information,
        'events': events,
        'using': using
    }
    return json_list

def request_to_class_event(json_request):
    event = Event()
    event_id = json_request.get('event_id', None)
    time = json_request.get('time', None)
    value = json_request.get('value', None)
    discripe = json_request.get('discripe', None)
    event.event_id = event_id
    event.time = time
    event.value = value
    event.discripe = discripe
    return event


def update_event(json_request,mongo,condition=None):
    event = request_to_class_event(json_request)
    user_datas_cursor = mongo.db.user.find(condition)
    user_data={"data":[dict_serializable(user_datas) for user_datas in user_datas_cursor]}
    user_data["events"].append(event)
    mongo.db.user.update(condition, {"$set": {"events": user_data["events"]}})
    datas = mongo.db.user.find(condition)
    return datas

def find_event(mongo,condition):
    event = mongo.db.user.find(condition,{"events":1})
    return event

def delete_event(mongo,condition):
    try:
        mongo.db.user.update(condition, {"$set":{"event_using":False}})
    except:
        return False
    return True