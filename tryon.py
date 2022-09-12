from flask import Blueprint, request

tryon = Blueprint('tryon', __name__, url_prefix='/tryon')


@tryon.route('/', method=['GET'])
def try_on():
    user_id = request.args['user_id']
    top = request.args['top']
    bottom = request.args['bottom']
    outer = request.args['outer']
