from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import accounts
import oauth
import recommendation
from config import DB_URL

app = Flask(__name__)
CORS(app)
app.register_blueprint(oauth.kakao)
app.register_blueprint(accounts.accounts)
app.register_blueprint(recommendation.recommendation)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
