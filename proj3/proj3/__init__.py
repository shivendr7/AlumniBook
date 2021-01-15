from flask import Flask, render_template, url_for, request, session, flash, redirect
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os


app=Flask(__name__)
app.secret_key="FarmPlus"
#app.permanent_session_lifetime=timedelta(hours=5)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config['UPLOAD_FOLDER']="B:/python/Flask/proj3/static/uploads"
#Path to your app folder/static/uploads

db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column('id',db.Integer,primary_key=True)
    name=db.Column('name',db.String(100),nullable=False)
    email=db.Column('email',db.String(100),nullable=False,unique=True)
    residence=db.Column('residence',db.String(100),nullable=False)
    password=db.Column('password',db.String(100),nullable=False)

    def __init__(self, name, email,residence, password):
        self.name=name
        self.email=email
        self.residence=residence
        self.password=password

class Story(db.Model):
    id=db.Column('storyid',db.Integer,primary_key=True)
    title=db.Column('title',db.String(150),nullable=False)
    content=db.Column('content',db.String(1000),nullable=False)
    time=db.Column('storytime',db.Time,nullable=False)
    email=db.Column('email',db.String(100),nullable=False)

    def __init__(title,content,time,email):
        self.title=title
        self.content=content
        self.time=time
        self.email=email



@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        residence=request.form['farm']
        password=request.form['password']
        #session.permanent=True
        find_user=User.query.filter_by(email=email).first()
        if find_user:
            if password==find_user.password:
                session['email']=find_user.email
                return redirect(url_for('dash'))
            else:
                flash('Invalid login')
                return render_template('index.html',LorD='Login')
        user=User(name=name, email=email, residence=residence, password=password)
        db.session.add(user)
        db.session.commit()
        session['email']=user.email
        return redirect(url_for('dash'))

    else:
        if 'email' in session:
            return render_template('index.html',LorD='Dashboard')
        return render_template('index.html',LorD='Login')

@app.route('/dash')
def dash():
    if 'email' in session:
        email=session['email']
        user=User.query.filter_by(email=email).first()
        return render_template('dash.html',name=user.name,email=user.email,storysentival=0.0,onstorysentival=0.0,laststorysentival=0.0,onlaststorysentival=0.0)
    else :
        return redirect(url_for('home'))

@app.route('/history')
def hist():
    return render_template('history.html')

@app.route('/story')
def story():
    return render_template('stories.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/feed')
def feed():
    return render_template('infeed.html')

@app.route('/upload',methods=['POST','GET'])
def uploadtest():
    if request.method=='POST':
        if 'file' not in request.files:
            flash('no file')
            return render_template('home.html',filename='axe',ext='png')
        else:
            file=request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('home.html',filename=filename[:filename.index('.')],ext=filename[filename.index('.')+1:])
    else:       
        return render_template('home.html',filename='axe',ext='png')

db.create_all()
app.run(use_reloader=False, port='800')
