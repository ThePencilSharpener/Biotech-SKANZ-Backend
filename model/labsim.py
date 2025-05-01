# post.py
from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from model.user import User

class LabSim(db.Model):
    """
    Labsim Model
    
    The LabSim class represents an individual lab simulation attempt by a user.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the lab attempt.
        _name1 (db.Column): An integer representing the user who created the lab attempt (foreign key to users.id).
        _points (db.Column): A string representing the points scored in the lab attempt.
    """
    __tablename__ = 'labsim'

    id = db.Column(db.Integer, primary_key=True)
    _name1 = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _points = db.Column(db.String(255), nullable=False)

    def __init__(self, name1, points):
        """
        Constructor, 1st step in object creation.
        """
        self._name1 = name1
        self._points = points

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the LabSim class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"LabSim(id={self.id}, name1={self._name1}, points={self._points})"

    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        
        Uses:
            The User.query method to retrieve the user object.
        
        Returns:
            dict: A dictionary containing the lab simulation data, including the user's name.
        """
        user = User.query.get(self._name1)
        data = {
            "id": self.id,
            "user_name": user.name if user else None,  # Retrieve the user's name
            "points": self._points
        }
        return data
    
    def update(self):
        """
        The update method commits the transaction to the database.
        
        Uses:
            The db ORM method to commit the transaction.
        
        Raises:
            Exception: An error occurred when updating the object in the database.
        """
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """
        The delete method removes the object from the database and commits the transaction.
        
        Uses:
            The db ORM methods to delete and commit the transaction.
        
        Raises:
            Exception: An error occurred when deleting the object from the database.
        """    
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def initLabSim():
    """
    The initPosts function creates the Post table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Post objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """        
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        
        p1 = LabSim(name1=1, points="1")  
        p2 = LabSim(name1=2, points="2")
        p3 = LabSim(name1=3, points="3")
        p4 = LabSim(name1=1, points="4")
        
        for post in [p1, p2, p3, p4]:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {post.uid}")