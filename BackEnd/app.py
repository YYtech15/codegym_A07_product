# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, flash, session
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from flask_cors import CORS, cross_origin
import sys

USER='root'
PASSWORD='tanisun1150'
HOST = 'localhost'
DATABASE = 'mysql://root:tanisun1150@localhost/test1'


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "secret"
"""csrf = CSRFProtect(app)"""
"""CORS(app)"""

metadata = MetaData()

engine = create_engine(DATABASE)
session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = session.query_property()

class User(Base):
    __tablename__ = 'Users'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String(200), nullable=true)
    mail = Column('mail', String(200), nullable = false)
    password = Column('password', String(200), nullable=false)
    def __init__(self, mail, password):
        self.mail = mail
        self.password = password

    def __repr__(self):
        return 'User'

class LoginUser(UserMixin, User):
    def get_id(self):
        return self.id

def main(args):
    Base.metadata.create_all(bind=engine)

#このファイルを直接実行したとき、mainメソッドでテーブルを作成する
if __name__ == "__main__":
    main(sys.argv)

@login_manager.user_loader
def load_user(user_id):
    return LoginUser.query.filter(LoginUser.id == user_id).one_or_none()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    input_mail = request.form['mailAddress']
    input_password = request.form['password']

    if(input_mail == None or input_password == None):
        return render_template('login.html', error="please enter all content")

    if (session.query(User).filter(input_mail == User.mail).one_or_none() == None):
        return render_template('login.html', error="No mail found")

    if (session.query(User).filter(input_password == User.password).one_or_none() == None):
        return render_template('login.html', error="password incorrect")

    return render_template('member.html')


@app.route('/signup', methods=['GET'])
def signup():
    return redirect('/signup')

@app.route('/signup', methods=["POST"])
def signup_post():

    input_mail = request.form['mailAddress']
    input_password = request.form['password']
    input_rePassword = request.form['re_password']

    if input_mail == None or input_password == None or input_rePassword == None:
        return render_template('signup.html', error="Pease enter all information")
    
    if input_password != input_rePassword:
        return render_template('signup.html', error="rechecking password failed")
    
    user = User(input_mail, input_password) 
    session.add(user)
    session.commit()

    return render_template('login.html', error="signup succeeded!")


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
