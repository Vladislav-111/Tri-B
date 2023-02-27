from flask import url_for
from app import db
import sqlalchemy as sa
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import os
from markdown import markdown

class Medic(db.Model, UserMixin):
    __tablename__ = 'medics'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name =  db.Column(db.String(30), nullable=False)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name])

    def __repr__(self):
        return '<Medic %r>' % self.login

class Med(db.Model):
    __tablename__ = 'meds'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text(),nullable=False)
    way = db.Column(db.Text(), nullable=False)
    side = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<Med %r>' % self.name

class Checkup(db.Model):
    __tablename__ = 'checkups'

    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.Text(), nullable=False)
    symptom = db.Column(db.Text(), nullable=False)
    comment = db.Column(db.Text(), nullable=False)
    place = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    med_id = db.Column(db.Integer, db.ForeignKey('meds.id'))
    medic_id = db.Column(db.Integer, db.ForeignKey('medics.id'))

    customer = db.relationship('Customer')
    med = db.relationship('Med')
    medic = db.relationship('Medic')


    def __repr__(self): 
        return '<Checkup %r>' % self.id

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)

    def __repr__(self): 
        return '<Customer %r>' % self.first_name

