#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：back-end 
@File    ：media.py
@Author  ：alex
@Date    ：2022/11/4 16:52 
"""
from flask import request
import json

from flaskz.log import flaskz_logger
from flaskz.models import model_to_dict
from flaskz.rest import init_model_rest_blueprint, get_rest_log_msg
from flaskz.utils import create_response
from sqlalchemy import desc, asc

from app.modules import Media
from . import api_bp


# init_model_rest_blueprint(Media, api_bp, '/media', '')


@api_bp.route('/media')
def get_all_media():
    result = Media.query_all()
    res_data = model_to_dict(result[1])
    flaskz_logger.debug(get_rest_log_msg('Query all Media data', None, result[0], res_data))
    return create_response(result[0], res_data)


@api_bp.route('/media/recent', methods=['POST'])
def get_recent_media():
    request_json = request.json
    page = request_json.get('page')
    search = request_json.get('search')
    filters = []
    for key, value in search.items():
        filters.append(key + '="' + value + '"')
    req_log_data = json.dumps(request_json)
    result = Media.query_pss({
        'order': desc(Media.add_time).nullslast(),
        'offset': page.get('offset'),
        'limit': page.get('limit'),
        'filter_ands': filters
    })
    res_data = result[1]
    if result[0] is True:
        res_data['data'] = model_to_dict(res_data['data'])

    flaskz_logger.debug(get_rest_log_msg('Query pss Media data', None, req_log_data, res_data))
    return create_response(result[0], res_data)
