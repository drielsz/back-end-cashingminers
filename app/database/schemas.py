import marshmallow as ma
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column, ForeignKey


from app.database.configuration import engine

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    uuid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(Text, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password= password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('uuid', 'name', 'email', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many = True)