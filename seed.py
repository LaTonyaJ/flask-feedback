from models import User, db
from app import app

db.drop_all()
db.create_all()

me = User(first_name='LaTonya', last_name='Johnson',
          username='tink870', password='tink', email='latonya.johnson@gmail.com')

db.session.add(me)
db.session.commit()
