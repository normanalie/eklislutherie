# For cPanel:
# "Execute python script" section:
#   create_db.py
#   Run Script

from app import db, create_app
db.create_all(app=create_app())