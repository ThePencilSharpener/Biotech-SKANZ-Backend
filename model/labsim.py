from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from __init__ import app, db
import logging

class LabSim (db.Model):
   
    __tablename__ = 'labsim'
    id = db.Column(db.Integer, primary_key=True)
    dna = db.Column(db.String(255), nullable=False)
    age = db.Column(db.String(255), nullable=False)
    def __init__(self, dna, age, ):
        self.dna = dna
        self.age = age
    def __repr__(self):
       
        return f"<LabSim(id={self.id}, dna='{self.dna}', age='{self.age})>"
    def create(self):
       
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    def read(self):
       
        return {
            "id": self.id,
            "dna": self.dna,
            "age": self.age,
        }
    def update(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            logging.error(f"Error creating hobby: {e}")
            db.session.rollback()
            return False
    def delete(self):
       
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            logging.error(f"Error deleting hobby: {e}")
            db.session.rollback()
            return False
   
    @staticmethod
    def restore(data):
        with app.app_context():
            db.session.query(LabSim).delete()
            db.session.commit()

            restored_facts = {}
            for fact_data in data:
                fact = LabSim(
                    dna=fact_data['dna'],
                    age=fact_data['age']
                )
                fact.create()
                restored_facts[fact_data['id']] = fact

            return restored_facts
def initLabSim():
   
    with app.app_context():
        db.create_all()  # Create the database and tables
        # Sample test data
        quizzes = [
            LabSim(dna="T", age="1"),
            LabSim(dna="G", age="2"),
            LabSim(dna="C", age="3"),
            LabSim(dna="A", age="4"),
        ]
        for quiz in quizzes:
            try:
                quiz.create()
                print(f"Created quiz: {repr(quiz)}")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Record already exists or error occurred: {str(e)}")