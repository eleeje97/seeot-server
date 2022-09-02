from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import oauth
from config import DB_URL

app = Flask(__name__)
app.register_blueprint(oauth.kakao)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/user', methods=['GET'])
def get_users():
    from model import User

    users = User.query.all()
    return users


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
