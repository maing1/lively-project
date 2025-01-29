#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# # Local imports
# from app import app
# from models import db, User, Post, Like, Comment,Follower

# if __name__ == '__main__':
#     fake = Faker()
#     with app.app_context():
#         print("Starting seed...")
#         # Seed code goes here!

from app import app, db  # Import the app and db from your main app file
from models import User, Post, Like, Comment, Follower # Import your models

# Create the seed data
def seed_data():
    with app.app_context():
        # Drop existing tables and recreate them
        print("Dropping existing tables...")
        db.drop_all()
        print("Creating tables...")
        db.create_all()

        # Seed Users
        print("Seeding users...")
        user1 = User(username="user1", email="user1@example.com", password="password")
        user2 = User(username="user2", email="user2@example.com", password="password")
        user3 = User(username="user3", email="user3@example.com", password="password")

        db.session.add_all([user1, user2, user3])
        db.session.commit()
        print("Users added to the session.")

        # Seed Posts
        print("Seeding posts...")
        post1 = Post(content="First Post!", user_id=user1.id)
        post2 = Post(content="Second Post!", user_id=user2.id)
        post3 = Post(content="Third Post!", user_id=user3.id)

        db.session.add_all([post1, post2, post3])
        db.session.commit()
        print("Posts added to the session.")

        # Seed Likes
        print("Seeding likes...")
        like1 = Like(user_id=user1.id, post_id=post2.id)  # User1 likes User2's post
        like2 = Like(user_id=user2.id, post_id=post3.id)  # User2 likes User3's post
        like3 = Like(user_id=user3.id, post_id=post1.id)  # User3 likes User1's post

        db.session.add_all([like1, like2, like3])
        db.session.commit()
        print("Likes added to the session.")

        # Seed Comments
        print("Seeding comments...")
        comment1 = Comment(content="Nice post!", user_id=user1.id, post_id=post2.id)
        comment2 = Comment(content="Awesome!", user_id=user2.id, post_id=post3.id)
        comment3 = Comment(content="Great thoughts!", user_id=user3.id, post_id=post1.id)

        db.session.add_all([comment1, comment2, comment3])
        db.session.commit()
        print("Comments added to the session.")

                # Seed Followers
        print("Seeding followers...")
        follower1 = Follower(follower_id=user1.id, followed_id=user2.id)  # User1 follows User2
        follower2 = Follower(follower_id=user2.id, followed_id=user3.id)  # User2 follows User3
        follower3 = Follower(follower_id=user3.id, followed_id=user1.id)  # User3 follows User1

        db.session.add_all([follower1, follower2, follower3])
        db.session.commit()
        print("Followers added to the session.")

# Run the seed function
if __name__ == "__main__":
    print("Starting the seeding process...")
    seed_data()
    print("Seeding process complete!")

        
