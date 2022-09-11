from flask import Blueprint, request

from key.file_path import USER_CLOTHES_DIR

recommendation = Blueprint('recommendation', __name__, url_prefix='/recommendation')


@recommendation.route('/', methods=['GET'])
def get_recommendations():
    from model import User
    import app
    db = app.db

    user_id = request.args['user_id']
    user = User.query.filter(User.id == user_id).first()
    if user is None:
        return {'message': 'Authentication Failed!'}, 401

    if user.gender == 'female':
        print('여자 옷 추천')
    else:
        print('male이거나 성별이 없으면 남자 옷 추천')

    return user.gender


@recommendation.route('/save', methods=['GET'])
def save_recommendation():
    import os
    import shutil
    from model import MyClothes
    import app
    db = app.db

    user_id = request.args['user_id']
    img_path = request.args['img_path']

    # user_id 예외처리: 해당 user가 DB에 없는 경우
    # img_path 예외처리: 해당 파일이 없는 경우


    # dir_name = os.path.join(USER_CLOTHES_DIR, user_id, 'recommendation')
    # os.makedirs(dir_name, exist_ok=True)
    #
    # file_name = img_path.split('/')[-1].split('.')[0]
    # output_path = os.path.join(dir_name, file_name + '.jpg')
    # uniq = 1
    # while os.path.exists(output_path):
    #     output_path = os.path.join(dir_name, file_name + str(uniq) + '.jpg')
    #     uniq += 1
    #
    # shutil.copy(img_path, output_path)


    # season 추출
    season = 'any'

    ### DB에 저장 ###
    clothes = MyClothes(user_id=user_id,
                        origin_img_path=img_path,
                        season=season,
                        is_user_img=0)
    db.session.add(clothes)
    db.session.commit()

    return {'message': 'Image Save Success!',
            'user_id': user_id,
            'file_path': img_path}
