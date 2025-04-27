from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_login import LoginManager
from datetime import timedelta
from flask_session import Session


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db?check_same_thread=False'
app.config['SECRET_KEY'] = 'bdfc368df5d3fc142b5d53cb'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)
app.app_context().push()

csrf = CSRFProtect(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

Session(app)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400 

from module import routes
