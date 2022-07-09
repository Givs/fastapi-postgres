from database import SessionLocal
from errors.error_instance import error_instance
from sqlalchemy import or_

import models

db = SessionLocal()


def create_paper(paper):
    new_paper = models.Paper(
        author_id=paper.author_id,
        title=paper.title,
        sumary=paper.sumary
    )

    find_author_id = db.query(models.Author).filter(models.Author.id == paper.author_id).count()
    if not find_author_id:
        error_instance(404, "Author not found.")

    db.add(new_paper)
    db.commit()
    return new_paper


def get_and_search_papers(term):
    if term:
        term = term.replace("'", '')
        papers = db.query(models.Paper).filter(
            or_(models.Paper.sumary.like("%" + term + "%"), models.Paper.title.like("%" + term + "%"))).all()
        if not papers:
            error_instance(404, "Papers not found with this term :( Try another one!")
    else:
        papers = db.query(models.Paper).all()

    return papers


def get_a_paper(paper_id):
    paper = db.query(models.Paper).filter(models.Paper.id == paper_id).first()

    if not paper:
        error_instance(404, "Paper not found.")

    return paper


def update_paper(paper_id, paper):
    paper_to_update = db.query(models.Paper).filter(models.Paper.id == paper_id).first()

    find_author_id = db.query(models.Author).filter(models.Author.id == paper.author_id).count()
    if not find_author_id:
        error_instance(404, "Author not found.")

    if not paper_to_update:
        error_instance(404, "Paper not found.")

    paper_to_update.author_id = paper.author_id
    paper_to_update.title = paper.title
    paper_to_update.sumary = paper.sumary

    db.commit()

    return paper_to_update


def delete_paper(paper_id):
    paper_to_delete = db.query(models.Paper).filter(models.Paper.id == paper_id).first()

    if not paper_to_delete:
        error_instance(404, "Paper not found.")

    db.delete(paper_to_delete)
    db.commit()
    return paper_to_delete
