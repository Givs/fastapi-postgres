from src.database.database import SessionLocal
from src.errors.error_instance import error_instance


import src.database.models

db = SessionLocal()


def create_author(author):
    new_author = src.database.models.Author(
        name=author.name
    )

    db.add(new_author)
    db.commit()

    return new_author


def search_author(term):
    if term:
        term = term.replace("'", '')
        authors = db.query(src.database.models.Author).filter(src.database.models.Author.name.like("%" + term + "%")).all()
        if not authors:
            error_instance(404, "Authors not found with this term :( Try another one!")
    else:
        authors = db.query(src.database.models.Author).all()

    return authors


def get_an_author(author_id):
    author = db.query(src.database.models.Author).filter(src.database.models.Author.id == author_id).first()

    if not author:
        error_instance(404, "Author not found")

    return author


def update_author(author_id, author):
    author_to_update = db.query(src.database.models.Author).filter(src.database.models.Author.id == author_id).first()

    if not author_to_update:
        error_instance(404, "Author not found")

    author_to_update.name = author.name
    db.commit()

    return author_to_update


def delete_author(author_id):
    author_to_delete = db.query(src.database.models.Author).filter(src.database.models.Author.id == author_id).first()

    if not author_to_delete:
        error_instance(404, "Author not found")

    db.delete(author_to_delete)
    db.commit()
    return author_to_delete
