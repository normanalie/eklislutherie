# For cPanel:
# "Execute python script" section:
#   create_db.py
#   Run Script
from app import db, create_app

def create():
    db.create_all(app=create_app())

if __name__=="__main__":
    create()