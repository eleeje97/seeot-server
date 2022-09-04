from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import accounts
import oauth
from config import DB_URL

app = Flask(__name__)
app.register_blueprint(oauth.kakao)
app.register_blueprint(accounts.accounts)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
