from flask_restful import Resource, reqparse
from flask import jsonify, make_response
import traceback
from server import db
from models import UserModel

#
# Create a parser for handling request arguments
# Preventing SQL injection in Python, only accept these field
#
parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

#
# Define a class for handling individual user resources
#
class User(Resource):
    #
    # Handle HTTP GET request to retrieve a user by ID
    #
    def get(self, id):
        ls = []
        user = UserModel.query.filter_by(id = id, deleted = None).first()
        ls.append(user)
        return jsonify({'data' : list(map(lambda user : user.serialize(), ls))})
    
    #
    # Handle HTTP PATCH request to update a user's details
    #
    def patch(self, id):
        arg  = parser.parse_args()
        user = UserModel.query.filter_by(id = id, deleted = None).first()
        if arg['name'] != None:
            user.name = arg['name']
        if arg['gender'] != None:
            user.gender = arg['gender']
        if arg['birth'] != None:
            user.birth = arg['birth']
        if arg['note'] != None:
            user.note = arg['note']
        
        response = {}
        status_code = 200
        try:
            db.session.commit()
            response['msg'] = 'Success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'Failed'
        
        return make_response(jsonify(response), status_code)
    
    # 
    # Handle HTTP DELETE request to hard delete a user
    # This is hard delete
    # 
    def delete(self, id):
        user = UserModel.query.filter_by(id = id, deleted = None).first()
        
        response = {}
        status_code = 200
        try:
            db.session.delete(user)
            db.session.commit()
            response['msg'] = 'Success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'Failed'
            
        return make_response(jsonify(response), status_code)
    

#
# Define a class for handling multiple users
#
class Users(Resource):        
    #
    # Handle HTTP GET request to retrieve all users
    #
    def get(self):
        users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
        return jsonify({'data' : list(map(lambda user : user.serialize(), users))})
    
    #
    # Handle HTTP POST request to create a new user
    #
    def post(self):
        arg = parser.parse_args()
        user = {
            'name' : arg['name'],
            'gender' : arg['gender'] or 0,
            'birth' : arg['birth'] or '1900-01-01',
            'note' : arg['note']
        }
        
        response = {}
        status_code = 200
        try:
            new_user = UserModel(name = user['name'], gender = user['gender'], birth = user['birth'], note = user['note'])
            db.session.add(new_user)
            db.session.commit()
            response['msg'] = 'Success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'Failed'
            
        return make_response(jsonify(response), status_code)