## Python Science Question Sample API endpoint
# Python Science Question Sample API endpoint
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from science_question import ScienceQuestionModel  # Your updated model with saved weights

science_api = Blueprint('science_api', __name__, url_prefix='/api')
api = Api(science_api)

class ScienceAPI:
    class _Predict(Resource):
        def post(self):
            """
            POST request to predict the topic of a science question.
            Expects a JSON body with a 'question' field.
            """
            data = request.get_json()
            question = data.get('question', '')

            if not question:
                return jsonify({"error": "Missing or empty 'question' field"}), 400

            model = ScienceQuestionModel.get_instance()
            response = model.predict(question)

            return jsonify(response)

    api.add_resource(_Predict, '/predict')
