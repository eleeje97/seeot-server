from flask import Blueprint, redirect, session, request

from kakao_controller import Oauth
from key.kakao_key import CLIENT_ID, REDIRECT_URI, LOGOUT_REDIRECT_URI

kakao = Blueprint('kakao', __name__, url_prefix='/kakao')


@kakao.route('/login')
def kakao_login():
    kakao_oauth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    return redirect(kakao_oauth_url)


@kakao.route('/callback')
def callback():
    import app
    from model import User

    db = app.db

    print(request)
    code = request.args["code"]

    oauth = Oauth()
    auth_info = oauth.auth(code)

    # error 발생 시 로그인 페이지로 redirect
    if "error" in auth_info:
        print("Kakao Login Error!")
        return {'message': 'Authentication Failed!'}, 404

    user = oauth.userinfo("Bearer " + auth_info['access_token'])
    print(user)

    kakao_account = user["kakao_account"]
    profile = kakao_account["profile"]
    nickname = profile["nickname"]
    id = str(user["id"])

    user = User.query.filter(User.id == id).first()
    if user is None:
        # 유저 테이블에 추가
        user = User(id=id, nickname=nickname, gender=None, full_body_img_path=None)
        db.session.add(user)
        db.session.commit()

    # session['user_id'] = user.id
    message = 'Kakao Login Success!'
    value = {"status": 200, "result": "success", "msg": message}

    print(value)

    return redirect('http://127.0.0.1:5050/')


@kakao.route('/logout')
def kakao_logout():
    kakao_oauth_url = f"https://kauth.kakao.com/oauth/logout?client_id={CLIENT_ID}&logout_redirect_uri={LOGOUT_REDIRECT_URI}"

    if session.get('email'):
        session.clear()
        value = {"status": 200, "result": "success"}
    else:
        value = {"status": 404, "result": "fail"}

    print('[Logout]', value)
    return redirect(kakao_oauth_url)
