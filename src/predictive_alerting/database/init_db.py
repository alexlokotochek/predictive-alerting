from database import db
from models import *


db.create_all()
db.session.commit()

print('Success!')
