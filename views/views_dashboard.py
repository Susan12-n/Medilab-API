# import required modules
import pymysql
from flask_restful import *
from flask import *
from functions import *
import pymysql.cursors

# jwt packages
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required
# lab signup resource
class LabSignup(Resource):
    def post(self): 
        data = request.json
        lab_name = data["lab_name"]
        email = data["email"]
        phone = data["phone"]
        permit_id = data["permit_id"]
        password = data["password"]

        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        cursor = connection.cursor()

        response = password_validity(password)
        if response:
            if check_phone(phone):
                # phone is correct
                sql = "INSERT INTO laboratories(lab_name,email,phone,permit_id,password) VALUES(%s,%s,%s,%s,%s)"
                data = (lab_name,email,encypt(phone),permit_id,hash_password(password))

                try:
                    cursor.execute(sql,data)
                    connection.commit()
                    code = gen_random()
                    send_sms(phone, '''Thankyou for joining medilab.
                             Your secret No: {}. Do not share. '''. format(code))
                    return jsonify({"message":"Lab signup successfull"})
                except:
                    connection.rollback()
                    return jsonify({"message":"lab signup failed"})

            else:
                # phone is not in correct format
                return jsonify({"message":"Invalid phone enter +254.."})    

        else:
           return jsonify({"message":response})
        
class Labsignin(Resource):
    def post(self):
        data = request.json
        email = data["email"]
        password = data["password"]

        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        sql = "select * from laboratories where email = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, email)

        if cursor.rowcount == 0:
            return jsonify({"Message": "Email does not exist"})
        else:
            # check password
            lab = cursor.fetchone()
            hashed_password = lab["password"]
            is_match_password = hash_verify(password, hashed_password)
            if is_match_password == True:
                access_token = create_access_token(identity=lab, fresh=True)
                return jsonify({"access_token":access_token,'Lab':lab})
            elif is_match_password == False:
                return jsonify({"Message": "Login failed"})
            else:
                return jsonify({"Message": "Something went wrong"})

# view lab profile using lab id
class Labprofile(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        lab_id = data["lab_id"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        sql = "select * from laboratories where lab_id = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, lab_id)
        if cursor.rowcount == 0:
            return jsonify({"Message": "lab does not exist"})
        else:
            lab = cursor.fetchone()
            return jsonify({"message":lab})
        
class AddLabTest(Resource):
        @jwt_required(fresh=True)
        def post(self):
            data = request.json
            lab_id = data["lab_id"]
            test_name = data["test_name"]
            test_description = data["test_description"]
            test_cost = data["test_cost"]
            test_discount = data["test_discount"]

            connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
            sql = "INSERT INTO lab_tests(lab_id,test_name,test_description,test_cost,test_discount) VALUES(%s,%s,%s,%s,%s)"
            cursor = connection.cursor()

            try:
                cursor.execute(sql, (lab_id,test_name,test_description,test_cost,test_discount))
                connection.commit()
                return jsonify ({"message":"Lab test added succesfully"})
            except:
                connection.rollback()
                return jsonify({"message":"Failed to add lab test"})
            

class ViewLabTest(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        lab_id = data["lab_id"]

        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        sql = "select * from lab_tests where lab_id = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql,lab_id)

        if cursor.rowcount == 0:
            return jsonify({"message":"No lab test found"})
        else:
            lab = cursor.fetchall()
            return jsonify({"message":lab})
        
class ViewLabBooking(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        lab_id = data["lab_id"]

        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        sql = "select * from bookings where lab_id = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql,lab_id)  

        if cursor.rowcount == 0:
            return jsonify({"message":"No bookings found"})
        else:
            bookings = cursor.fetchall()
            # associate member_id with the booking
            # we want to loop all the booking
            for booking in bookings:
                member_id = booking["member_id"]
                # return jsonify(member_id)
                sql = "select * from member where member_id = %s"
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                cursor.execute(sql,member_id)
                member = cursor.fetchone()
                # the result is attached to booking dictionary under key
                booking["key"] = member
                # return jsonify(member)
                
            import json
            # we want to pass our bookings to json.dumps
            ourbookings = json.dumps(bookings, indent=1, sort_keys=True, default=str)
            return json.loads(ourbookings)
        
class AddNurse(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        surname = data["surname"]
        others = data["others"]
        gender = data["gender"]
        lab_id = data["lab_id"]

        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        sql = "insert into nurses (surname, others, gender, lab_id) values (%s, %s, %s, %s)"
        cursor = connection.cursor()

        try:
            cursor.execute(sql, (surname, others, gender, lab_id))
            connection.commit()
            return jsonify ({"message":"Nurse added successfully"})
        except:
            connection.rollback()
            return jsonify({"message":"Failed to add nurse"})
        
class ViewNurse(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        nurse_id = data["nurse_id"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        sql = "select * from nurses where nurse_id = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, nurse_id)
        if cursor.rowcount == 0:
            return jsonify({"Message": "Nurse does not exist"})
        else:
            nurse = cursor.fetchall()
            return jsonify({"message":nurse})



class TaskAllocation(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        nurse_id = data["nurse_id"]
        invoice_no = data["invoice_no"]

        connection = pymysql.connect(host='localhost', user='root', password='', database='medilab')
        sql = "insert into nurse_lab_allocation(nurse_id, invoice_no) values (%s, %s)"
        cursor = connection.cursor()

        try:
            cursor.execute(sql, (nurse_id, invoice_no))
            connection.commit()
            return jsonify({"message":"allocation successful"})
        except:
            connection.rollback()
            return jsonify({"message":"Failed to allocate task"})




# from flask import request, jsonify
# from flask_restful import Resource
# import pymysql
# import os
# from werkzeug.utils import secure_filename

# # Define the directory where you want to save uploaded files
# UPLOAD_FOLDER = 'static/images'
# ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# class AddPhoto(Resource):
#     def post(self):
#         if 'file' not in request.files:
#             return jsonify({"Message": "No file part"})
        
#         file = request.files['file']
#         shoe_id = request.form.get("shoe_id")

#         if not shoe_id or not file:
#             return jsonify({"Message": "Shoe ID and file are required"})

#         if file.filename == '':
#             return jsonify({"Message": "No selected file"})
        
#         if not allowed_file(file.filename):
#             return jsonify({"Message": "Invalid file type"})

#         # Connect to the database
#         connection = pymysql.connect(
#             host='shoeapp.mysql.pythonanywhere-services.com',
#             user='shoeapp',
#             password='12345678Aa@',
#             database='shoeapp$default'
#         )

#         cursor = connection.cursor()

#         # Check if the shoe_id exists
#         check_sql = "SELECT COUNT(*) FROM shoes WHERE shoe_id = %s"
#         cursor.execute(check_sql, (shoe_id,))
#         result = cursor.fetchone()
#         if result[0] == 0:
#             return jsonify({"Message": "Shoe ID does not exist"})

#         # Save the file
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(UPLOAD_FOLDER, filename)
#         file.save(file_path)

#         # Insert into the database
#         insert_sql = "INSERT INTO shoe_photos (shoe_id, photo_url) VALUES (%s, %s)"
#         photo_url = file_path  # Use the saved file path as the photo_url

#         try:
#             cursor.execute(insert_sql, (shoe_id, photo_url))
#             connection.commit()
#             return jsonify({"Message": "Photo added successfully"})
#         except Exception as e:
#             connection.rollback()
#             print(e)  # Log the exception for debugging
#             return jsonify({"Message": "Photo not added"})
#         finally:
#             cursor.close()
#             connection.close()


import os
from werkzeug.utils import secure_filename


# Define the directory where you want to save uploaded files
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class AddShoeWithPhoto(Resource):
    def post(self):
        # Get shoe details from the request
        data = request.form.to_dict()
        category_id = data.get("category_id")
        name = data.get("name")
        price = data.get("price")
        description = data.get("description")
        brand_name = data.get("brand_name")
        quantity = data.get("quantity")  # Get quantity from the request

        # Handle file upload
        if 'file' not in request.files:
            return jsonify({"Message": "No file part"})

        file = request.files['file']

        if not category_id or not name or not price or not description or not brand_name or not quantity or not file:
            return jsonify({"Message": "All fields and file are required"})

        if file.filename == '':
            return jsonify({"Message": "No selected file"})

        if not allowed_file(file.filename):
            return jsonify({"Message": "Invalid file type"})

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # # Construct the URL path for the image
        # base_url = "https://shoeapp2.pythonanywhere.com/static/images/"
        photo_url = file_path

        # Connect to the database
        # connection = pymysql.connect(
        #     host='shoeapp2.mysql.pythonanywhere-services.com',
        #     user='shoeapp2',
        #     password='12345678Aa@',
        #     database='shoeapp2$default'
        # )
        connection = pymysql.connect(host='localhost', user='root', password='', database='shoeapp')

        cursor = connection.cursor()

        try:
            # Insert shoe details into the database
            insert_shoe_sql = """
                INSERT INTO shoes (category_id, name, price, description, brand_name, quantity, photo_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_shoe_sql, (category_id, name, price, description, brand_name, quantity, photo_url))
            connection.commit()

            return jsonify({"Message": "Shoe and photo added successfully"})
        except Exception as e:
            connection.rollback()
            print(e)  # Log the exception for debugging
            return jsonify({"Message": "Shoe and photo not added"})
        finally:
            cursor.close()
            connection.close()



            








        
               




        

