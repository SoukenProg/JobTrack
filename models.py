from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationshi

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Companies(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)

    website = db.Column(db.String(255))
    location = db.Column(db.String(255))
    memo = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.now(),nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    applications = db.relationship('Applications', backref='companies', cascade='all, delete-orphan')
    def __repr__(self):
        return f"Company {self.company_name}"

class Applications(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    company_name = db.Column(db.String(100),db.ForeignKey('companies.company_name'), nullable=False)

    job_title = db.Column(db.String(100), nullable=False)
    application_route = db.Column(db.String(100))
    status = db.Column(db.String(50), nullable=False,default='未応募')

    application_date = db.Column(db.DateTime, default=datetime.now(),nullable=False)
    deadline = db.Column(db.DateTime,default=datetime.now())

    salary = db.Column(db.String(100))
    work_style = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    company = db.relationship(
        'Companies',
        backref='applications',
    )
    interviews = db.relationship(
        'Interview',
        backref='applications',
        cascade='all, delete-orphan'
    )
    def __repr__(self):
        return f"<Application {self.company_name} / {self.status}>"

class Interviews(db.Model):
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)

    interview_date = db.Column(db.DateTime,nullable=False)
    interview_type = db.Column(db.String(50),nullable=False)
    interview_round = db.Column(db.String(50),nullable=False)

    inteviewer = db.Column(db.String(50))
    location = db.Column(db.String(50))

    prepare_memo = db.Column(db.Text)
    result_memo = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    application = db.relationship(
        'Applications',
        backref='interviews',
    )
    def __repr__(self):
        return f"<Interview {self.interview_round}  {self.interview_date}>"

