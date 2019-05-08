from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from json import dumps
from flask_jsonpify import jsonify
from flask_marshmallow import Marshmallow

import os
import json

db_connect = create_engine('sqlite:///user.db')
app = Flask(__name__)
api = Api(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'user.db')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    age = db.Column(db.Integer)

    def __init__(self,id, first_name,last_name, email,gender,age):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.age = age

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','first_name','last_name', 'email','gender','age')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

# endpoint to get user by id
@app.route("/users/getId/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

# endpoint to get user detail by first_name
@app.route("/users/first_name/<val>", methods=["GET"])
def user_first_name(val):
    user = User.query.filter_by(first_name = val).first()
    return user_schema.jsonify(user)

# endpoint to get user detail by last_name
@app.route("/users/last_name/<val>", methods=["GET"])
def user_last_name(val):
    user = User.query.filter_by(last_name = val).first()
    return user_schema.jsonify(user)

# endpoint to get user detail by email
@app.route("/users/email/<val>", methods=["GET"])
def user_email(val):
    user = User.query.filter_by(email = val).first()
    return user_schema.jsonify(user)

# endpoint to get user detail by gender
@app.route("/users/gender/<val>", methods=["GET"])
def user_gender(val):
    user = User.query.filter_by(gender = val).all()
    return user_schema.jsonify(user, many=True)

# endpoint to get user detail by age
@app.route("/users/age/<val>", methods=["GET"])
def user_age(val):
    user = User.query.filter_by(age = val).all()
    return user_schema.jsonify(user, many=True)

# endpoint to get user detail by age range
@app.route("/users/age/<val1>/<val2>", methods=["GET"])
def user_age_range(val1,val2):
    user = User.query.filter((User.age >= val1) & (User.age <= val2)).all()
    return user_schema.jsonify(user, many=True)

# endpoint to create new user
@app.route("/users", methods=["POST"])
def add_user():
    id = request.json['id']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    gender = request.json['gender']
    age = request.json['age']
    
    new_user = User(id, first_name,last_name, email,gender,age)

    db.session.add(new_user)
    db.session.commit()

    return 'Success'


# endpoint to update user
@app.route("/users/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    gender = request.json['gender']
    age = request.json['age']

    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.gender = gender
    user.age = age

    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to delete user
@app.route("/users/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)



# class Users(Resource):
#     def get(self):
#         conn = db_connect.connect() # connect to database
        
#         query = conn.execute("select * from users") # This line performs query and returns json result
#         result = {'users': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
#         return jsonify(result)      
#     def post(self):
#         conn = db_connect.connect()
#         sql = 'select * from users '
#         print(request.json)
#         if "id" in request.form:   
#             pass                  
#             user_id = request.form['id']   
#             # sql = 'select * from users where id = 1'
#             sql += 'where id =%d '  %int(user_id)
#         elif "firstName" in request.form:   
#             pass                  
#             user_name = request.form['firstName']   
#             sql += " where first_name =  '%s'" % user_name
#         elif "lastName" in request.form:   
#             pass                  
#             last_name = request.form['lastName']   
#             sql += " where last_name =  '%s'" % last_name
#         elif "email" in request.form:   
#             pass                  
#             email = request.form['email']   
#             sql += " where email =  '%s'" % email 
#         elif "age" in request.form:   
#             pass                  
#             age = request.form['age']   
#             sql += " where age =  '%d'" %int(age)
        
#         elif "ageBetween1" in request.form:   
#             pass                  
#             ageFrom = request.form['ageBetween1']           
#             ageTo = request.form['ageBetween2']
#             sql += " where age >=  '%d'" %int(ageFrom) 
#             sql += " and age <=  '%d'" %int(ageTo)
        
#         elif "gender" in request.form:   
#             pass                  
#             gender = request.form['gender']    
#             sql += " where gender =  '%s'" % gender 
               

#         query = conn.execute(sql) # This line performs query and returns json result
#         result = {'users': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
#         return jsonify(result)
        
# class User(Resource):
#     def post(self):
#         conn = db_connect.connect()
#         print(request.json)
#         UserId = request.json['id']
#         FirstName = request.json['first_name']
#         LastName = request.json['last_name']
#         gender = request.json['gender']
#         age = request.json['age']        
#         Email = request.json['email']
#         query = conn.execute("insert into users values('{0}','{1}','{2}','{3}', \
#                              '{4}','{5}')".format(UserId,FirstName,LastName,
#                              gender, age, Email))
#         return {'status':'success'}

#     def put(self):
#         conn = db_connect.connect()
#         print(request.json)
#         UserId = request.json['id']
#         FirstName = request.json['first_name']
#         LastName = request.json['last_name']
#         gender = request.json['gender']
#         age = request.json['age']        
#         Email = request.json['email']
#         query = conn.execute("update users set first_name ='{1}', last_name = '{2}', gender ='{3}', \
#                              age ='{4}', email ='{5}' where id = '{0}' ".format(UserId,FirstName,LastName,
#                              gender, age, Email))
#         return {'status':'success'}

#     def delete(self):
#         conn = db_connect.connect()
#         print(request.json)
#         UserId = request.json['id']
#         FirstName = request.json['first_name']
#         LastName = request.json['last_name']
#         gender = request.json['gender']
#         age = request.json['age']        
#         Email = request.json['email']
#         query = conn.execute("delete from users where id = '{0}' ".format(UserId,FirstName,LastName,gender, age, Email))
#         return {'status':'success'}


# api.add_resource(Users, '/users_search') # secrch by post
# api.add_resource(User, '/user_management') # user management





if __name__ == '__main__':
    app.debug = True
    app.run(port='5002')