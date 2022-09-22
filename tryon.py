from flask import Blueprint, request

tryon = Blueprint('tryon', __name__, url_prefix='/tryon')


@tryon.route('/', methods=['GET'])
def try_on():
    print('Try On START!!!')

    from models.dior import run

#     user_id = request.args['user_id']
#     top = request.args['top']
#     bottom = request.args['bottom']
#     outer = request.args['outer']

    # 문서에 저장
    run.try_on(0, 1, 2, 1)

    return {'output_img': 'output_img_path'}

