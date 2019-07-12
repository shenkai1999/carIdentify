#≈Ì”¿≥¨
from exts import  db
class User(db.Model):
    __tablename__='webUser'
    name = db.Column(db.String(32), primary_key=True,autoincrement=True)
    password = db.Column(db.String(100),nullable=False)

