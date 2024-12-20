import pymysql
from flask_restful import Resource
from pymysql.err import MySQLError
from flask import *
import logging
from werkzeug.security import check_password_hash
# import JWT packages
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


from functions import *
#  Add a member class
# member_signup and member_signin

class MemberSignup(Resource):
    def post(self):
        # Get the data from the client.
        data = request.json
        surname = data.get("surname")
        others = data.get("others")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")
        location_id = data.get("location_id")

        # Validate the presence of required fields
        if not all([surname, others, email, phone, password, location_id]):
            return jsonify({"Message": "All fields are required"})

        # Check if the password is valid
        response = password_validity(password)
        if response != True:
            return jsonify({"Message": response})

        # Hash the password before storing it
        hashed_password = hash_password(password)

        # Connect to database
        connection = pymysql.connect(
            host='shoeapp2.mysql.pythonanywhere-services.com',
            user='shoeapp2',
            password='12345678Aa@',
            database='shoeapp2$default'
        )
        cursor = connection.cursor()

        try:
            # Insert into database
            sql = """
                INSERT INTO users (surname, others, email, phone, password, location_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            data = (surname, others, email, phone, hashed_password, location_id)
            cursor.execute(sql, data)
            connection.commit()
            return jsonify({"Message": "Registration successful. User saved"})
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Database error: {e}")
            return jsonify({"Message": "Registration failed. User not saved"})
        finally:
            cursor.close()
            connection.close()



class MemberSignin(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Validate the presence of required fields
        if not all([email, password]):
            return jsonify({'message': 'Email and password are required'})

        # Connect to database
        connection = pymysql.connect(
            host='shoeapp2.mysql.pythonanywhere-services.com',
            user='shoeapp2',
            password='12345678Aa@',
            database='shoeapp2$default'
        )
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        try:
            # Fetch the user based on email
            sql = "SELECT * FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            member = cursor.fetchone()

            if member is None:
                return jsonify({'message': 'User does not exist'})

            # Verify the password
            hashed_password = member['password']  # This Password is hashed
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                # Generate JSON Web Token
                access_token = create_access_token(identity=email, fresh=True)
                return jsonify({
                    'access_token': access_token,
                    'member': member
                })
            else:
                return jsonify({'message': 'Login Failed'})
        except pymysql.MySQLError as e:
            logging.error(f"Database error: {e}")
            return jsonify({'message': 'An error occurred'})
        finally:
            cursor.close()
            connection.close()


        
            
class MemberProfile(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        member_id = data["member_id"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='medilab')
        sql = "select * from members where member_id = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, member_id)
        if cursor.rowcount == 0:
            return jsonify({"Message": "Member does not exist"})
        else:
            member = cursor.fetchone()
            return jsonify({"message":member})

class AddDependant (Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        member_id = data["member_id"]
        surname = data["surname"]
        others = data["others"]
        dob  = data["dob"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='medilab')
        cursor = connection.cursor()
        sql = "insert into dependants (member_id, surname, others, dob) values (%s, %s, %s, %s)"
        data = (member_id, surname, others,dob)
        try:
            cursor.execute(sql, data)
            connection.commit()
            return jsonify({"Message":"POST SUCCESSFUL. Dependant saved"})

        except:
            connection.rollback( )
            return jsonify({"Message":"POST FAILED. Dependant not saved"})

class ViewDependants(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        member_id = data["member_id"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='medilab')
        sql = "select * from dependants where member_id = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, member_id)
        if cursor.rowcount == 0:
            return jsonify({"Message": "Member does not exist"})
        else:
            member = cursor.fetchall()
            return jsonify({"message":member})

class Laboratories(Resource):
    def get(self):
        connection = pymysql.connect(host='localhost', user='root', password='', database='medilab')
        sql = "select * from laboratories"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return jsonify({"Message":"No laboratories"})
        else:
            labs = cursor.fetchall()
            return jsonify(labs)

class LabTest(Resource):
    def post(self):
        data = request.json
        lab_id = data["lab_id"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='medilab')
        sql = "select * from lab_tests where lab_id = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, lab_id)
        if cursor.rowcount == 0:
            return jsonify({"Message": "No lab test found"})
        else:
            lab = cursor.fetchall()
            return jsonify({"message":lab})

class MakeBooking(Resource):
    def post(self):
        data = request.json
        member_id = data["member_id"]
        booked_for = data["booked_for"]
        dependant_id = data["dependant_id"]
        test_id = data["test_id"]
        appointment_date = data["appointment_date"]
        appointment_time = data["appointment_time"]
        where_taken = data["where_taken"]
        latitude = data["latitude"]
        longitude = data["longitude"]
        status = data["status"]
        lab_id = data["lab_id"]
        invoice_no = data["invoice_no"]
        
        connection = pymysql.connect(host='localhost', user='root', password='', database='medilab')
        cursor = connection.cursor()
        sql = "insert into bookings(member_id, booked_for, dependant_id, test_id, appointment_date, appointment_time, where_taken, latitude, longitude, status, lab_id, invoice_no) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (member_id, booked_for, dependant_id, test_id, appointment_date, appointment_time, where_taken, latitude, longitude, status, lab_id, invoice_no)

        try:
            cursor.execute(sql, data)
            connection.commit()
            return jsonify({"message":"Booking Verified"})
        
        except:
            connection.rollback()
            return jsonify({"message":"Booking Failed"})

class mybooking(Resource):
    def get(self):
        data = request.json
        member_id = data["member_id"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='medilab')
        sql = "select * from bookings where member_id = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, member_id)
        if cursor.rowcount == 0:
            return jsonify({"Message": "Booking does not exist"})
        else:
            bookings = cursor.fetchall()
            # date and time was not convertible to json
            # hence we use json.dumps and json.loads
            import json
            # we want to pass our bookings to json.dumps
            ourbookings = json.dumps(bookings, indent=1, sort_keys=True, default=str)
            return json.loads(ourbookings)

class payment(Resource):
    def post(self):
        data = request.json
        invoice_no = data["invoice_no"]
        amount = data["amount"]
        phone = data["phone"]
        mpesa_payment(amount, phone, invoice_no)
        return jsonify({"message":"Payment Successful"})