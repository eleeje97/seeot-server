from flask import Blueprint, request, render_template

from kakao_controller import Oauth
from key.file_path import USER_FULLBODY_DIR

accounts = Blueprint('accounts', __name__, url_prefix='/accounts')


@accounts.route('/kakao/login', methods=['GET'])
def kakao_login():
    import app
    from model import User

    db = app.db

    code = request.args['code']

    oauth = Oauth()
    auth_info = oauth.auth(code)
    # print(auth_info)

    if 'error' in auth_info:
        return {'message': 'Authentication Failed!'}, 401

    access_token = auth_info['access_token']
    refresh_token = auth_info['refresh_token']
    user_info = oauth.userinfo("Bearer " + access_token)

    kakao_account = user_info["kakao_account"]
    profile = kakao_account["profile"]

    id = str(user_info["id"])
    user = User.query.filter(User.id == id).first()
    if user is None:
        nickname = profile["nickname"]
        if kakao_account["has_gender"]:
            gender = kakao_account["gender"]
        else:
            gender = 'male'
        user = User(id=id,
                    nickname=nickname,
                    gender=gender,
                    full_body_img_path=None,
                    access_token=access_token,
                    refresh_token=refresh_token)
        db.session.add(user)
    else:
        user.nickname = profile["nickname"]
        user.access_token = access_token
        user.refresh_token = refresh_token

    db.session.commit()

    return {'message': 'Kakao Login Success!', 'user_id': id}


@accounts.route('/kakao/logout', methods=['GET'])
def kakao_logout():
    from model import User
    oauth = Oauth()

    user_id = request.args['user_id']
    user = User.query.filter(User.id == user_id).first()
    if user is None:
        return {'message': 'Authentication Failed!'}, 401

    access_token = user.access_token
    oauth.logout("Bearer " + access_token)

    return {'message': 'Kakao Logout Success!', 'user_id': user_id}



@accounts.route('/users', methods=['GET'])
def get_users():
    from model import User

    users = User.query.all()
    response = {'users': [i.as_dict() for i in users]}

    return response


@accounts.route('/userinfo', methods=['GET'])
def user_info():
    from model import User
    import app

    oauth = Oauth()
    db = app.db

    user_id = request.args['user_id']
    user = User.query.filter(User.id == user_id).first()
    if user is None:
        return {'message': 'Authentication Failed!'}, 401

    access_token = user.access_token
    user_info = oauth.userinfo("Bearer " + access_token)
    if 'code' in user_info:
        new_access_token = oauth.token(user.refresh_token)['access_token']
        user.access_token = new_access_token
        db.session.commit()

        user_info = oauth.userinfo("Bearer " + new_access_token)

    kakao_account = user_info['kakao_account']
    nickname = user.nickname
    gender = user.gender
    profile_image_url = kakao_account['profile']['profile_image_url']
    full_body_img_path = user.full_body_img_path

    response = {'user': {'id': user_id,
                         'nickname': nickname,
                         'gender': gender,
                         'profile_image_url': profile_image_url,
                         'full_body_img_path': full_body_img_path}}

    return response


@accounts.route('/update/profile', methods=['POST'])
def update_profile():
    import os
    from model import User
    import app
    from models.human_parsing import run

    db = app.db

    if request.method == 'POST':
        user_id = request.values['user_id']
        gender = request.values['gender']

        # DB에 update
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            return {'message': 'Authentication Failed!'}, 401

        if request.files:
            file = request.files['file']
            os.makedirs(USER_FULLBODY_DIR, exist_ok=True)
            filename = user_id + '.jpg'
            file.save(os.path.join(USER_FULLBODY_DIR, filename))

            file_path = USER_FULLBODY_DIR + '/' + filename
            user.full_body_img_path = file_path

            origin_img_path = file_path
            output_img_path = USER_FULLBODY_DIR + '/' + user_id + '.png'
            run.human_parsing(origin_img_path, output_img_path)
        else:
            file_path = 'No File Uploaded!'

        user.gender = gender
        db.session.commit()

        return {'message': 'Profile Updated!',
                'user_id': user_id,
                'gender': gender,
                'file_path': file_path}


# @accounts.route('')