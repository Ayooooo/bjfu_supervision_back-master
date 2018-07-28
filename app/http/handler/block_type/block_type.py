from app.http.handler.block_type import block_type_blueprint
from flask_pymongo import ObjectId
from flask import jsonify, request
from flask import url_for
from app.core.controllers.block_type_controller import insert_block_type, delete_block_type, find_block_type, \
    update_block_type, request_to_class, request_to_change
from app.core.controllers.common_controller import dict_serializable, UrlCondition, sort_limit, Paginate


@block_type_blueprint.route('/block_types')
def get_block_types():
    url_condition = UrlCondition(request.args)
    from run import mongo
    try:
        block_types = find_block_type(mongo, url_condition.filter_dict)
    except:
        return jsonify({
            'code':'500',
            'message':''
        })
    block_types = sort_limit(block_types, url_condition.sort_limit_dict)
    paginate = Paginate(block_types, url_condition.page_dict)
    prev = None
    if paginate.has_prev:
        prev = url_for('block_type_blueprint.get_block_types', _page=paginate.page - 1)
    next = None
    if paginate.has_next:
        next = url_for('block_type_blueprint.get_block_types', _page=paginate.page + 1)
    return jsonify({
        'code':'200',
        'message':'',
        'data':[dict_serializable(block_type) for block_type in block_types],
        'prev': prev,
        'next': next,
        'has_prev': paginate.has_prev,
        'has_next': paginate.has_next,
        'total': paginate.total,
        'page_num': paginate.page_num,
        'page_now': paginate.page,
        'per_page': paginate.per_page
    })


@block_type_blueprint.route('/block_types', methods=['POST'])
def new_block_type():
    from run import mongo
    block_type = request_to_class(request.json)
    try:
        insert_block_type(mongo, block_type)
    except:
        return jsonify({
            'code':'500',
            'message':''
        })
    return jsonify({
        'code':'200',
        'message':'',
        'data':[dict_serializable(block_type.model)]
    })


@block_type_blueprint.route('/block_types/<string:_id>')
def get_block_type(_id):
    from run import mongo
    try:
        block_types = find_block_type(mongo, {'_id':ObjectId(_id)})
    except:
        return jsonify({
            'code':'500',
            'message':''
        })
    return jsonify({
        'code':'200',
        'message':'',
        'data':[dict_serializable(block_type) for block_type in block_types]
    })


@block_type_blueprint.route('/block_types/<string:_id>', methods= ['DELETE'])
def del_block_type(_id):
    from run import mongo
    try:
        delete_block_type(mongo, {'_id':ObjectId(_id)})
    except:
        return jsonify({
            'code':'500',
            'message':''
        })
    return jsonify({
        'code':'200',
        'message':'',
        'data':[]
    })


@block_type_blueprint.route('/block_types/<string:_id>', methods=['PUT'])
def change_block_type(_id):
    from run import mongo
    change = request_to_change(request.json)
    try:
        update_block_type(mongo, {'_id':ObjectId(_id)}, change)
    except:
        return jsonify({
            'code':'500',
            'message':''
        })
    return jsonify({
        'code':'200',
        'message':'',
        'data':[]
    })