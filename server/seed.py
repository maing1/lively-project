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
from models import User, Post  # Import your models

# Create the seed data
def seed_data():
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()

        print("Creating tables...")
        db.create_all()

        # Seed Users
        print("Seeding users...")
        user1 = User(username="johndoe", email="john@example.com", password="password123")
        user2 = User(username="janedoe", email="jane@example.com", password="securepassword")
        user3 = User(username="bobby99", email="bobby@example.com", password="mypassword")

        # Seed Posts
        print("Seeding posts...")
        post1 = Post(content="Hello world! This is my first post.", user_id=1)
        post2 = Post(content="Loving the Lively app!", user_id=2)
        post3 = Post(content="Anyone up for a coding challenge?", user_id=3)
        post4 = Post(content="Beautiful day outside!", user_id=1)

        # Add users to the session
        db.session.add_all([user1, user2, user3])
        print("Users added to the session.")

        # Add posts to the session
        db.session.add_all([post1, post2, post3, post4])
        print("Posts added to the session.")

        # Commit the changes
        db.session.commit()
        print("Database seeded successfully!")

# Run the seed function
if __name__ == "__main__":
    print("Starting the seeding process...")
    seed_data()
    print("Seeding process complete!")

        
