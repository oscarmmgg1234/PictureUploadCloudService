#dependecies
import base64
from form import LoginForm,imageBody,RegisterForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager
from flask import Flask,request,session,redirect,render_template
from flask_restful import Api
from dbMODEL import User,API
from flask_bootstrap import Bootstrap


#init Flask
app = Flask(__name__)
api = Api(app)

#init database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DATABASE/ADMIN.sqlite'

db = SQLAlchemy(app)

#init Bootstrap
Bootstrap(app)

#init flask-login
app.config['SECRET_KEY'] = 'BALLLLLLLLS'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

entry = False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#login routes
@app.route('/image_API/login',methods=["POST","GET"])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()


        if form.username.data:
            session['username'] = form.username.data
            return redirect('/uploads')

        else:
            return '<h1>Invalid username or password</h1>'
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/uploads', methods=['POST', 'GET'])
def upload():
    form = imageBody()

    if session['username'] == None:
        return redirect('/image_API/login')

    if request.method == 'POST':
        img = request.files['image']
        str64 = base64.urlsafe_b64encode(img.read())
        newUpload = API(author=session['username'], imgID=str64, description=form.description.data, name=form.name.data)
        db.session.add(newUpload)
        db.session.commit()
        form.description.data = ''

    return render_template('index.html', form=form)


@app.route('/image_API/register/newUser', methods=['POST', 'GET'])
def newUser():
    form = LoginForm()
    if request.method == 'POST':
        session['username'] = current_user.username
        return render_template('login.html', form=form)

    return render_template('newUser.html')


@app.route('/image_API/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST' and form.validate():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/image_API/register/newUser')
    # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username')
    session.clear()
    return redirect('/image_API/login')


@app.route('/image_API/get/image', methods=['POST', 'GET'])
def get():
    if request.method == 'POST':
        req_data = request.get_json()
        username = req_data['username']
        password = req_data['password']
        name = req_data['referenceImageName']

        user = User.query.filter_by(password=password).first()
        if user.password == password:
            if user.username == username:
                img = API.query.filter_by(name=name).first()
                id = base64.urlsafe_b64decode(img.imgID)

            return id


@app.route('/app/get/post', methods=["POST", "GET"])
def appPost():
    if request.method == "POST":
        req_data = request.get_json()
        username = req_data['username']
        password = req_data['password']
        usr = User.query.filter_by(username=username).first()
        if username == usr.username:
            if password == usr.password:
                entry = True
            else:
                entry = False
    else:
        return None


@app.route('/app/get/<string:username>/<string:password>/<string:name>')
def getAPP(username, password, name):
    user = User.query.filter_by(username=username).first()

    img = API.query.filter_by(name=name).first()
    id = base64.urlsafe_b64decode(img.imgID)

    if user.username == username:
        if user.password == password:
            return id


@app.route('/app/get/entry')
def getEntry():
    return entry;





if __name__ == '__main__':
    app.run()
