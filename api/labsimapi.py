from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # Used for REST API building
from __init__ import app  # Ensure __init__.py initializes your Flask app
from model.coolfacts import CoolFacts
from model.labsim import LabSim
from api.jwt_authorize import token_required

# Blueprint for the API
coolfacts_api = Blueprint('coolfacts_api', __name__, url_prefix='/api')
labsim_api = Blueprint('labsim_api', __name__, url_prefix='/api')
api_coolfacts = Api(coolfacts_api)  # Attach Flask-RESTful API to the Blueprint
api_labsim = Api(labsim_api)  # Attach Flask-RESTful API to the Blueprint

class CoolFactsAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Create a new post object using the data from the request
            post = CoolFacts(age=data['age'], coolfacts=data['coolfacts'])
            # Save the post object using the Object Relational Mapper (ORM) method defined in the model
            post.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(post.read())

        @token_required()
        def put(self):
            data = request.get_json()
            if not data or not data.get("age") or not data.get("coolfacts"):
                return jsonify({"message": "Coolfact and age are required to update"}), 400
            coolfact = CoolFacts.query.filter_by(coolfacts=data["coolfacts"], age=data["age"]).first()
            if not coolfact:
                return jsonify({"message": "Coolfact and age not found"}), 404
            # Update the object's attributes
            coolfact.coolfacts = data["new_coolfacts"]
            coolfact.age = data["new_age"]
            if coolfact.update():
                return jsonify({"message": "Coolfact and age updated", "old_coolfact": data["coolfacts"], "new_coolfact": coolfact.coolfacts, "old_age": data["age"], "new_age": coolfact.age})

        @token_required()
        def get(self):
            try:
                # Query all entries in the BinaryHistory table
                entries = CoolFacts.query.all()
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
            post = CoolFacts.query.get(data['id'])
            # Delete the post using the ORM method defined in the model
            post.delete()
            # Return response
            return jsonify({"message": "Post deleted"})

    api_coolfacts.add_resource(_CRUD, '/coolfacts')

class LabSimAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            if not data or not data.get("dna") or not data.get("age"):
                return jsonify({"message": "DNA and age are required"}), 400
            
            # Create a new LabSim object using the data from the request
            lab_sim = LabSim(dna=data['dna'], age=data['age'])
            try:
                lab_sim.create()
                # Return response to the client in JSON format
                return jsonify(lab_sim.read()), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @token_required()
        def put(self):
            data = request.get_json()
            if not data or not data.get("id") or not data.get("dna") or not data.get("age"):
                return jsonify({"message": "ID, DNA, and age are required to update"}), 400
            
            # Find the LabSim entry by ID
            lab_sim = LabSim.query.get(data["id"])
            if not lab_sim:
                return jsonify({"message": "LabSim entry not found"}), 404
            
            # Update the object's attributes
            lab_sim.dna = data["dna"]
            lab_sim.age = data["age"]
            if lab_sim.update():
                return jsonify({"message": "LabSim entry updated", "updated_entry": lab_sim.read()})
            else:
                return jsonify({"message": "Error updating LabSim entry"}), 500

        @token_required()
        def get(self):
            try:
                # Query all entries in the LabSim table
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
            if not data or not data.get("id"):
                return jsonify({"message": "ID is required to delete"}), 400
            
            # Find the LabSim entry by ID
            lab_sim = LabSim.query.get(data['id'])
            if not lab_sim:
                return jsonify({"message": "LabSim entry not found"}), 404
            
            # Delete the entry
            if lab_sim.delete():
                return jsonify({"message": "LabSim entry deleted"})
            else:
                return jsonify({"message": "Error deleting LabSim entry"}), 500

    api_labsim.add_resource(_CRUD, '/labsim')

if __name__ == '__main__':
    app.run(debug=True)