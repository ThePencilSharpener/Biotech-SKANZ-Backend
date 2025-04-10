from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from __init__ import app, db
import logging

class LabSim (db.Model):
   
    __tablename__ = 'labsim'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    points = db.Column(db.String(255), nullable=False)
    def __init__(self, name, points, ):
        self.name = name
        self.points = points
    def __repr__(self):
       
        return f"<LabSim(id={self.id}, name='{self.name}', points='{self.points})>"
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
            "name": self.name,
            "points": self.points,
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
                    name=fact_data['name'],
                    points=fact_data['points']
                )
                fact.create()
                restored_facts[fact_data['id']] = fact

            return restored_facts
def initLabSim():
   
    with app.app_context():
        db.create_all()  # Create the database and tables
        # Sample test data
        quizzes = [
            LabSim(name="John", points="1"),
            LabSim(name="Jack", points="2"),
            LabSim(name="Jake", points="3"),
            LabSim(name="Jane", points="4"),
        ]
        for quiz in quizzes:
            try:
                quiz.create()
                print(f"Created quiz: {repr(quiz)}")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Record already exists or error occurred: {str(e)}")