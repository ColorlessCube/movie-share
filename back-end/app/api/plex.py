#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：back-end 
@File    ：plex.py
@Author  ：alex
@Date    ：2022/11/3 09:15 
"""
import datetime
import math
import os
import shutil

import requests
from flask import current_app
from flaskz.utils import api_request, create_response, get_dict_mapping, ins_to_dict
from flaskz.log import flaskz_logger
from xml.etree.ElementTree import fromstring, ElementTree

from app.api import api_bp
from app.modules import Media
from app.utils import map_dict_key, check_dict_update


@api_bp.route('/library/update')
def update_library():
    """
    Get movie or show info from plex library, update in db.
    Music and Photo are not supported at present.
    :return: update
    """
    data = {}
    library_xml_response = plex_api_request('/library/sections/all')
    plex_libraries = get_library_id(library_xml_response)
    for plex_library in plex_libraries:
        library_id = plex_library.get('id')
        library_type = plex_library.get('type')
        media_xml_response = plex_api_request('/library/sections/{}/all'.format(library_id))
        if library_type == 'movie':
            plex_movies = plex_xml_info_parse(media_xml_response, xml_tag='Video')
            movie_update_res = _update_library(plex_movies)
            data['movie'] = movie_update_res
        elif library_type == 'show':
            plex_shows = plex_xml_info_parse(media_xml_response, xml_tag='Directory')
            show_update_res = _update_library(plex_shows)
            data['show'] = show_update_res
    flaskz_logger.info('INFO: Update library info.\nDATA: {}'.format(data))
    return create_response(True, data)


@api_bp.route('/image/update')
def update_image():
    """
    Sync media art and thumb images from plex.
    :return:
    """
    res, medias = Media.query_all()
    if res:
        for media in medias:
            # pool = ThreadPoolExecutor(max_workers=current_app.config.get('MAX_DOWNLOAD_THREAD'))
            # for media in medias:
            #     pool.submit(plex_file_download, media.thumb, '{}.thumb.jpg'.format(media.id))
            #     pool.submit(plex_file_download, media.art, '{}.art.jpg'.format(media.id))
            # pool.shutdown()
            if media.thumb:
                plex_file_download(media.thumb, '{}.thumb.jpg'.format(media.id))
            if media.art:
                plex_file_download(media.art, '{}.art.jpg'.format(media.id))
    return create_response(True, '123')


# plex attributes => db columns mapping
attributes_mapping = {
    'ratingKey': 'id',
    'title': 'title',
    'originalTitle': 'original_title',
    'type': 'type',
    'genre': 'genre',
    'summary': 'summary',
    'studio': 'studio',
    'tagline': 'tagline',
    'contentRating': 'content_rating',
    'audienceRating': 'audience_rating',
    'userRating': 'user_rating',
    'thumb': 'thumb',
    'art': 'art',
    'duration': 'duration',
    'viewCount': 'view_count',
    'leafCount': 'episode_count',
    'viewedLeafCount': 'viewed_episode_count',
    'childCount': 'season_count',
    'year': 'year',
    'originallyAvailableAt': 'available_time',
    'addedAt': 'add_time',
    'updatedAt': 'update_time',
    'lastViewedAt': 'last_view_time',
    'lastRatedAt': 'last_rate_time',
}


def plex_xml_info_parse(response, xml_tag):
    """
    Parse movie info from plex api response.
    :param response: xml
    :param xml_tag: Video or Directory
    :return: movie info dict list
    """
    movie_info_list = []
    tree = ElementTree(fromstring(response))
    for elem in tree.iter(tag=xml_tag):
        attributes = elem.attrib
        genre_info = []
        for genre in elem.iter(tag='Genre'):
            genre_info.append(genre.attrib.get('tag'))
        attributes['genre'] = ','.join(genre_info)
        # update plex attribute to db column name
        movie_info = map_dict_key(attributes, attributes_mapping)
        movie_info = movie_info_format(movie_info)
        movie_info_list.append(movie_info)
    return movie_info_list


def movie_info_format(info):
    """
    Process movie info, some origin value's type is not in accordance with db value's type.
    :param info: origin movie info
    :return:
    """
    for key, value in info.items():
        if value:
            if key == 'id':
                info[key] = int(value)
            if '_time' in key and '-' not in value:
                format_time = datetime.datetime.fromtimestamp(int(value))
                info[key] = format_time
            if key == 'duration':
                duration = math.floor(int(value) / 1000 / 60)
                info[key] = duration
            if key == 'audience_rating':
                info[key] = float(value)
            if key == 'user_rating':
                info[key] = float(value)
            if key == 'view_count':
                info[key] = int(value)
            if key == 'season_count':
                info[key] = int(value)
            if key == 'episode_count':
                info[key] = int(value)
            if key == 'viewed_episode_count':
                info[key] = int(value)
    return info


def _update_library(plex_infos):
    """
    If plex info not in db, add it, otherwise update it.
    :param plex_infos:
    :return:
    """
    add_infos = []
    update_infos = []
    res, medias = Media.query_all()
    if res:
        info_id_map = get_dict_mapping(ins_to_dict(medias), 'id')
        for plex_info in plex_infos:
            db_media = info_id_map.get(plex_info.get('id'))
            if db_media:
                flag, media_info = check_dict_update(db_media, plex_info)
                if flag:
                    update_infos.append(media_info)
            else:
                add_infos.append(plex_info)
        Media.bulk_add(add_infos)
        Media.bulk_update(add_infos)
    data = {
        'add': len(add_infos),
        'update': len(update_infos)
    }
    return data


def get_library_id(library_xml_response):
    """
    Get plex library id.
    Like movie, show, music and etc.
    :return:
    """
    tree = ElementTree(fromstring(library_xml_response))
    library_ids = []
    for elem in tree.iter(tag='Directory'):
        library_ids.append({
            'id': elem.attrib.get('key'),
            'type': elem.attrib.get('type')
        })
    return library_ids


def plex_api_request(url, **kwargs):
    """
    Add the information required by the plex api.
    :param url:
    :return:
    """
    if url.endswith('/'):
        url = url[:-1]
    url = url + '?X-Plex-Token=' + current_app.config.get('PLEX_TOKEN')
    response = api_request(base_url=current_app.config.get('PLEX_BASE_URL'), url=url, method='GET', **kwargs)
    return response


def plex_file_download(url, file_name):
    """
    Download file from plex, add to given dir.
    :param url:
    :param file_name:
    :return:
    """
    if url.endswith('/'):
        url = url[:-1]
    base_url = current_app.config.get('PLEX_BASE_URL')
    url = base_url + url
    url = url + '?X-Plex-Token=' + current_app.config.get('PLEX_TOKEN')
    with requests.get(url=url, stream=True) as source:
        local_path = os.path.join(current_app.config.get('PLEX_IMAGE_DIR'), file_name)
        with open(local_path, 'wb') as file:
            shutil.copyfileobj(source.raw, file)
