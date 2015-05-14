from app import app, db
from app.models import *

# Make sure to start from a completely empty database
# Inside psql, use command "DROP DATABASE <DATABASE NAME>;" to completely remove the database
# Then use command "CREATE DATABASE <DATABASE NAME>;" to recreate a fresh one

# Create the initial database tables
db.drop_all()
db.create_all()

# Create the user and admin roles
user_role = Role(name='user', description='user')
admin_role = Role(name='admin', description='admin')
db.session.add(user_role)
db.session.add(admin_role)
db.session.commit()
