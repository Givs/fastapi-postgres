from database import Base
from sqlalchemy import String, Boolean, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    office = Column(String(255))

    def __repr__(self):
        return f"<User id={self.id} name={self.name} email={self.email} password={self.password} isSuperUser={self.office}"


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    paper = relationship("Paper", back_populates="owner")

    def __repr__(self):
        return f"<User id={self.id} name={self.name}"


class Paper(Base):
    __tablename__ = 'papers'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    title = Column(String(255), nullable=False)
    sumary = Column(String(255), nullable=False)

    owner = relationship("Author", back_populates="paper")

    def __repr__(self):
        return f"<User id={self.id} name={self.title}"

