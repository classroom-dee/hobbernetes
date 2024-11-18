from flask import Blueprint, render_template, jsonify, request
from .models import Widget
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/widgets', methods=['GET'])
def get_widgets():
    widgets = Widget.query.all()
    return jsonify([
        {'id': w.id, 'name': w.name, 'description': w.description, 'iframe_code': w.iframe_code}
        for w in widgets
    ])