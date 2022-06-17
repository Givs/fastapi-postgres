from database import Base
from sqlalchemy import String, Boolean, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    office = Column(String(255))
    author = relationship("Author")
    paper = relationship("Paper")

    def __repr__(self):
        return f"<User name={self.name} email={self.email} password={self.password} isSuperUser={self.office}"


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    fk_user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(255), nullable=False)
    paper = relationship("Paper")

    def __repr__(self):
        return f"<User name={self.name} email={self.fk_user_id}"

class Paper(Base):
    __tablename__ = 'papers'
    id = Column(Integer, primary_key=True)
    fk_user_id = Column(Integer, ForeignKey("users.id"))
    fk_author_id = Column(Integer, ForeignKey("authors.id"))
    title = Column(String(255), nullable=False)
    sumary = Column(String(255), nullable=False)



