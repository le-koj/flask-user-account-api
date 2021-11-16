### This package is a user-database API 
### Its a simple interface for performing user-account CRUD operations

from flask import Flask
from requests import status_codes
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import database_exists
import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
    """
        model to represent the user table

        parameters:
            id: Integer,
            first_name: string,
            last_name: string,
            email: string
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_date = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return {
                "First Name": f"{UserModel.first_name}",
                "Last Name": f"{UserModel.last_name}",
                "Email": f"{UserModel.email}",
                "Date Created": f"{UserModel.created_date}",
                "Date Updated": f"{UserModel.updated_date}"     
                }

#db.create_all()
if database_exists('sqlite:///database.db'):
    print(f"\n--------\n Database True \n------\n")
else:
    print(f"\n--------\n Database False \n------\n")
    #db.create_all()
    print(f"\n--------\n Database Created \n------\n")


# reqparse to enforce table fields
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("first_name", type=str, help="First Name of the user required", required=True)
user_put_args.add_argument("last_name", type=str, help="Last Name of the user required", required=True)
user_put_args.add_argument("email", type=str, help="Email of the user required", required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("first_name", type=str, help="First Name of the user ", required=False)
user_update_args.add_argument("last_name", type=str, help="Last Name of the user", required=False)
user_update_args.add_argument("email", type=str, help="email of the user", required=False)
#user_update_args.add_argument("updated_date")
#users = {}

# table fields json representation
# used with marshal_with
resource_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'created_date': fields.DateTime,
    'updated_date': fields.DateTime
}

response_fields = {
    "status_code": fields.Integer
}

def abort_user_id_not_exist(user):
    if not user:
        abort(404, message="user does not exit...")

def abort_if_user_exits(user_id):
    if UserModel.query.filter_by(id=user_id).first():
        abort(409, message="user already exists with ID...")

def abort_email_constraint(email):
    if UserModel.query.filter_by(email=email).first():
        abort(409, message="Email already exists...")


class User(Resource):

    @marshal_with(resource_fields)
    def get(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="Could not find user with that id")
        return user

    @marshal_with(resource_fields)
    def put(self, user_id):
        args = user_put_args.parse_args()
        abort_if_user_exits(user_id)
        abort_email_constraint(args['email'])
        user = UserModel(id=user_id, first_name=args['first_name'], last_name=args['last_name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(resource_fields)
    def patch(self, user_id):
        args = user_update_args.parse_args()

        abort_email_constraint(args['email'])

        # verify user existance
        user = UserModel.query.filter_by(id=user_id).first()

        abort_user_id_not_exist(user)

        # update database table fields    
        if args['first_name']:
            user.first_name = args['first_name']
          
        if args['last_name']:
            user.last_name = args['last_name']
           
        if args['email']:
            user.email = args['email']

        # update update_date if changes are made to table
        if args['email'] or args['first_name'] or args['last_name']:
            user.updated_date = datetime.datetime.now()

        db.session.commit() # commit updates to database

        return user

    def delete(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        abort_user_id_not_exist(user)
        db.session.delete(user)
        db.session.commit()
        return '', 204

api.add_resource(User, "/user/<int:user_id>")

if __name__ == "__main__":
    app.run(debug=True)