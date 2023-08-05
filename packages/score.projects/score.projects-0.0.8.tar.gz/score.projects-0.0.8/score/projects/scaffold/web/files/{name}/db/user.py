from .storable import Storable
from score.auth import ActorMixin
from sqlalchemy import Column
from sqlalchemy_utils.types.password import PasswordType


class Actor(Storable, ActorMixin):
    pass


class User(Actor):
    password = Column(PasswordType(schemes=['pbkdf2_sha512']))
