import datetime

from flask import render_template, current_app, request, jsonify, session

from info import db
from info.models import User
from info.response_code import RET
from . import index_blu


@index_blu.route('/')
def index():
    data = {}
    return render_template('index/index.html',data=data)