from flask import Flask, render_template, request
from markupsafe import escape
from flask import request, redirect, url_for
from db import user_table
import json

user_collection = user_table()

app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# @app.route("/<name>")
# def hello(name):
#         return f"Hello, {escape(name)}!"
    
# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return f'User {escape(username)}'

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return f'Post {post_id}'

# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
#     return f'Subpath {escape(subpath)}'

# @app.route('/hello/')
@app.route('/')
def hello():
    return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'success post'


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         # username = request.form['username']
#         # password = request.form['password']
        
#         # for x in user_collection.find():
#         #     if x['username'] == 'linhphan' and x['password'] == '123456':
#         #         return 'True'
#         return 'False'
#     else:
#         return 'error'
#     # return json.load(user_collection.find_one())
    
    # return user_collection.find_one()["username"]
