from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # Used for REST API building
from __init__ import app  # Ensure __init__.py initializes your Flask app
from model.labsim import LabSim
from api.jwt_authorize import token_required

# Blueprint for the API

labsim_api = Blueprint('labsim_api', __name__, url_prefix='/api')
api_labsim = Api(labsim_api)  # Attach Flask-RESTful API to the Blueprint
class LabSimAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Create a new post object using the data from the request
            post = LabSim(points=data['points'], name1=data['name1'])
            # Save the post object using the Object Relational Mapper (ORM) method defined in the model
            post.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(post.read())

        @token_required()
        def put(self):
            data = request.get_json()
            if not data or not data.get("points") or not data.get("name1"):
                return jsonify({"message": "name and points are required to update"}), 400
            old = LabSim.query.filter_by(name1=data["name1"], points=data["points"]).first()
            if not old:
                return jsonify({"message": "name and points not found"}), 404

            # Update the object's attributes
            old.name1 = data["new_name1"]
            old.points = data["new_points"]
            if old.update():
                #return "hello"
                return jsonify({"message": "name and points updated", "old name1": data["name1"], "new_name1": old.name1, "old_points": data["points"], "new_points": old.points})
           # coolfact.update({"coolfacts": data["coolfacts"], "points": data["points"]})

        @token_required()
        def get(self):
            try:
                # Query all entries in the BinaryHistory table
                entries = LabSim.query.all()
                # Convert the entries to a list of dictionaries
                results = [entry.read() for entry in entries]
                # Return the list of results in JSON format
                return jsonify(results)
            except Exception as e:
                # Return an error message in case of failure
                return jsonify({"error": str(e)}), 500

        @token_required()
        def delete(self):
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = LabSim.query.get(data['id'])
            # Delete the post using the ORM method defined in the model
            post.delete()
            # Return response
            return jsonify({"message": "Post deleted"})

    api_labsim.add_resource(_CRUD, '/labsim')

if __name__ == '__main__':
    app.run(debug=True)