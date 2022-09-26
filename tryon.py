from flask import Blueprint, request

tryon = Blueprint('tryon', __name__, url_prefix='/tryon')


@tryon.route('/', methods=['GET'])
def try_on():
    from model import User, MyClothes

    print('Try On START!!!')

    from models.dior import run

    user_id = request.args['user_id']
    top = request.args['top']
    bottom = request.args['bottom']

    # 문서에 저장
    user = User.query.filter(User.id == user_id).first()
    if user is None:
        return {'message': 'Authentication Failed!'}, 401
    print('fullbody:', user.full_body_img_path)

    top_clothes = MyClothes.query.filter(MyClothes.id == top).first()
    if top_clothes is None:
        return {'message': 'No Such Clothes!'}, 401
    print('top:', top_clothes.origin_img_path)

    bottom_clothes = MyClothes.query.filter(MyClothes.id == bottom).first()
    if bottom_clothes is None:
        return {'message': 'No Such Clothes!'}, 401
    print('bottom:', bottom_clothes.origin_img_path)



    # run.try_on(0, 1, 2, 1)

    return {'output_img': 'output_img_path'}

