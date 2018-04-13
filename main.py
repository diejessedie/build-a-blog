from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "JCJhmvHSY9uURT2v"
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner):
        self.name = name
        self.body = body
        self.completed = False
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route("/newblog", methods=['POST', 'GET'])
def newblog():
    owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        blog_name = request.form['blog-name']
        blog_body = request.form['blog-body']
        
        if blog_name == '' or blog_body == '':
            flash('Blog name and blog body required!', 'error')
            return render_template('new_blog.html',title="Post a New Blog!", 
            name=blog_name, body=blog_body)
        
        else:
            new_blog = Blog(blog_name, blog_body, owner)
            db.session.add(new_blog)
            db.session.commit()
            
            return render_template('single_post.html', blog=new_blog)

    return render_template('new_blog.html',title="Post a New Blog!", name=' ', body=' ')
    


@app.route("/blog", methods=['GET'])
@app.route('/', methods=['GET'])
def blogs():
    owner = User.query.filter_by(email=session['email']).first()

    blogs = Blog.query.filter_by(owner=owner).all()
    blogs = list(reversed(blogs))

    return render_template('all_blogs.html',title="Blogs!", 
        blogs=blogs)

@app.route("/post", methods=['GET'])
def single_post():
    id = request.args.get('id')
    blog = Blog.query.filter_by(id=id).first()

    return render_template('single_post.html', blog=blog)

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash('Logged in', "success")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')


    return render_template('login.html', title="Login")

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            flash('Registered and logged in', "success")
            return redirect('/')
        else:
            # TODO - user better response messaging
            flash('User already exists!', 'error')

    return render_template('register.html', title="Register")

if __name__ == '__main__':
    app.run()