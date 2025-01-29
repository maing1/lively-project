#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, jsonify, session
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import db, User, Post, Like, Comment, Follower

# Views go here!

@app.before_request
def check_login():
    if not session['user_id'] \
        and request.endpoint != 'login' \
        and request.endpoint != 'home'\
        and request.endpoint != 'users':
        return {"error":"unauthorized"},401

class Login(Resource):
    def post(self):
        username = request.get_json()['user_name']
        user =  User.query.filter(User.user_name==username).first()
        password = request.get_json()['password']
        if user.authenticate(password):
            session['user_id']= user.id
            return user.to_dict(),200
        
        return  {"error":"username or password is incorrect"},401

class Logout(Resource):
    def delete(self):
        session['user_id']=None
        return {"message":'logged out'},204

api.add_resource(Logout,"/logout", endpoint='logout')
api.add_resource(Login,'/login',endpoint='login')

class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict()
        else:
            return {"message":"the current user is unauthorized to access"},401

api.add_resource(CheckSession,'/session/check')

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

class Home(Resource):
    def get(self):
        posts = Post.query.all()
        return [
            {
                "id": post.id, 
             "content": post.content, 
             "username": post.user.username, 
             "image" : post.image, 
             "likes" : post.likes,
             "comments" : post.comments
            }
            for post in posts
        ]

api.add_resource(Home, '/posts')

class Posts(Resource):
    def post(self):
        data = request.get_json()

        content = data.get('content')
        image = data.get('image')
        user_id = data.get('user_id')


        user = User.query.get(user_id)
        if not user:
            return {"errors": ["Invalid User ID."]}, 400

        post = Post(
            content = content,
            image = image,
            user_id = user_id
        )
        db.session.add(post)
        db.session.commit()

        response = {
            "id" : post.id,
            "content" : post.content,
            "image" : post.image,
            "user" : {
                "id" : user.id,
                "username" : user.username,
            },
        }
        return make_response(jsonify(response), 201)

    def delete(self, id):
        post = Post.query.get(id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return make_response({"message": "Post deleted successfully"}, 200)
        return make_response({"error": "Post not found"}, 404)
    
api.add_resource(Posts, '/posts', '/posts/<int:id>')

class Users(Resource):
    def get(self):
        username = request.args.get('username')
        if username:
            users = User.query.filter(User.username.ilike(f"%{username}%")).all()
        else:
            users = User.query.all()

        return [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "bio": user.bio,
                "profile_picture": user.profile_picture,
                "followers_count": len(user.followers),
                "following_count": len(user.following),
                "posts": [
                    {"id": post.id, "content": post.content, "image": post.image}
                    for post in user.posts
                ],
            }
            for user in users
        ]
    def post(self):
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        bio = data.get('bio', "")
        profile_picture = data.get('profile_picture', "")

        if not username or not email or not password:
            return {"error": "Missing required fields"}, 400

        new_user = User(
            username=username,
            email=email,
            password=password,
            bio=bio,
            profile_picture=profile_picture
        )
        db.session.add(new_user)
        db.session.commit()

        response = {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
        return make_response(jsonify(response), 201)

api.add_resource(Users, '/users/<int:id>')

class Likes(Resource):
    def post(self):
        data = request.get_json()

        user_id = data.get('user_id')
        post_id = data.get('post_id')

        if not user_id or not post_id:
            return {"error": "Missing user_id or post_id"}, 400

        user = User.query.get(user_id)
        post = Post.query.get(post_id)

        if not user or not post:
            return {"error": "Invalid user_id or post_id"}, 400

        existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if existing_like:
            return {"error": "User already liked this post"}, 400

        new_like = Like(user_id=user_id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()

        return {"message": "Post liked successfully!"}, 201

    def delete(self):
        data = request.get_json()
        user_id = data.get('user_id')
        post_id = data.get('post_id')

        like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if like:
            db.session.delete(like)
            db.session.commit()
            return {"message": "Post unliked successfully!"}, 200
        return {"error": "Like not found"}, 404

api.add_resource(Likes, '/likes')

class Followers(Resource):
    def post(self):
        data = request.get_json()
        follower_id = data.get('follower_id')
        followed_id = data.get('followed_id')

        if not follower_id or not followed_id:
            return {"error": "Missing follower_id or followed_id"}, 400

        if follower_id == followed_id:
            return {"error": "You cannot follow yourself"}, 400

        follower = User.query.get(follower_id)
        followed = User.query.get(followed_id)
        if not follower or not followed:
            return {"error": "Invalid follower_id or followed_id"}, 400

        existing_follow = Follower.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
        if existing_follow:
            return {"error": "Already following this user"}, 400

        new_follow = Follower(follower_id=follower_id, followed_id=followed_id)
        db.session.add(new_follow)
        db.session.commit()

        return {"message": "Followed successfully!"}, 201

    def delete(self):
        """Unfollow a user"""
        data = request.get_json()
        follower_id = data.get('follower_id')
        followed_id = data.get('followed_id')

        follow = Follower.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
        if follow:
            db.session.delete(follow)
            db.session.commit()
            return {"message": "Unfollowed successfully!"}, 200
        return {"error": "Follow relationship not found"}, 404

api.add_resource(Followers, '/followers')

class Comments(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        post_id = data.get('post_id')
        content = data.get('content')

        if not user_id or not post_id or not content:
            return {"error": "Missing required fields"}, 400

        user = User.query.get(user_id)
        post = Post.query.get(post_id)
        if not user or not post:
            return {"error": "Invalid user_id or post_id"}, 400

        new_comment = Comment(user_id=user_id, post_id=post_id, content=content)
        db.session.add(new_comment)
        db.session.commit()

        return {
            "id": new_comment.id,
            "user_id": new_comment.user_id,
            "post_id": new_comment.post_id,
            "content": new_comment.content,
            "username": user.username
        }, 201

    def delete(self, id):
        """Delete a comment by ID"""
        comment = Comment.query.get(id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return {"message": "Comment deleted successfully"}, 200
        return {"error": "Comment not found"}, 404

api.add_resource(Comments, '/comments', '/comments/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)

