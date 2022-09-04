from flask import Blueprint, request

from kakao_controller import Oauth

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
        user = User(id=id, nickname=nickname, gender=gender, full_body_img_path=None, access_token=access_token)
        db.session.add(user)
    else:
        user.access_token = access_token

    db.session.commit()

    return {'message': 'Kakao Login Success!', 'user_id': id}


@accounts.route('/users', methods=['GET'])
def get_users():
    from model import User

    users = User.query.all()
    response = {'users': [i.as_dict() for i in users]}

    return response
