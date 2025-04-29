## Python Science Question Sample API endpoint
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource  # used for REST API building
from science_question import ScienceQuestionModel

# Import the ScienceQuestionModel class
# from model.science_question import ScienceQuestionModel

science_api = Blueprint('science_api', __name__,
                        url_prefix='/api')

api = Api(science_api)

class ScienceAPI:
    class _Predict(Resource):
        def post(self):
            """ Semantics: POST request to predict the topic of a science question.

            Sending a question to the server to get topic probabilities fits POST semantics.
            - POST body can hold larger text data easily.
            - HTTPS encrypts the body.
            - JSON makes communication simple and readable.
            """
            # Get the question data from the request
            data = request.get_json()
            question = data.get('question', '')

            # Get the singleton instance of the ScienceQuestionModel
            model = ScienceQuestionModel.get_instance()

            # Predict topic probabilities for the question
            response = model.predict(question)
            
            # Return the response as JSON
            return jsonify(response)

    api.add_resource(_Predict, '/predict')
