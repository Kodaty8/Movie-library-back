from sqlalchemy.orm import Session


def create(row, db: Session):
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def read(table, where, db: Session):
    res = db.query(table)
    for criteria in where:
        res = res.filter(table.__dict__[criteria[0]] == criteria[1])
    return res.all()
