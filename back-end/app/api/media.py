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

from app.modules import Media
from . import api_bp


@api_bp.route('/media')
def query_pss():
    result = Media.query_all()
    res_data = model_to_dict(result[1])
    flaskz_logger.debug(get_rest_log_msg('Query all Media data', None, result[0], res_data))
    return create_response(result[0], res_data)
