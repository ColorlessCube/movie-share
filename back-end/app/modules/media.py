#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：back-end 
@File    ：plex.py
@Author  ：alex
@Date    ：2022/11/3 10:22 
"""
from datetime import datetime

from flaskz.models import ModelBase, ModelMixin
from sqlalchemy import Column, Integer, String, DateTime, TEXT, FLOAT


class Media(ModelBase, ModelMixin):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64), nullable=False, unique=True)
    original_title = Column(String(64))
    # movie or show
    type = Column(String(32))
    content_rating = Column(String(32))
    summary = Column(TEXT)
    duration = Column(Integer())
    genre = Column(String(32))
    audience_rating = Column(FLOAT)
    user_rating = Column(FLOAT)
    thumb = Column(String(256))
    art = Column(String(256))
    studio = Column(String(32))
    tagline = Column(String(256))
    view_count = Column(Integer, default=0)
    year = Column(String(32))
    episode_count = Column(Integer)
    viewed_episode_count = Column(Integer)
    season_count = Column(Integer)
    available_time = Column(String(32))
    add_time = Column(DateTime)
    update_time = Column(DateTime)
    last_view_time = Column(DateTime)
    last_rate_time = Column(DateTime)
