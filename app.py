import sqlite3
from flask import Flask, jsonify, request


app = Flask(__name__)

#INDEX PAGE
@app.route('/')
def index_page():
    return 'This is first page'



#Connect and create table
def connect_to_bd():
    conn = sqlite3.connect('YOURBD.bd')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS YourTable (id INTEGER PRIMARY KEY, name CHAR(40), lastname CHAR(40))')
    conn.commit()
    return conn

# GET METHOD
@app.route('/get', methods=['GET'])
def get_method_api():
    conn = connect_to_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM YourTable')
    results = cursor.fetchall()
    # Convert for JSON STRUCTURE
    convert_json = [{'id':row [0] , 'name': row[1], 'lastname': row[2]} for row in results]
    return jsonify(convert_json)

# POST METHOD
@app.route('/post', methods=['POST'])
def post_method_api():
    new_data = request.get_json()
    # You can create a validation to not receive null values
    if new_data['name'] != "" and new_data['lastname'] != "":
        conn = connect_to_bd()
        cursor = conn.cursor()
        cursor.execute(""" INSERT INTO YourTable(name, lastname) VALUES(?,?) """, (new_data['name'], new_data['lastname'],))
        conn.commit()
        return jsonify({'mensage': 'Sucess'})
    else:
        return jsonify({'mensage': 'Error, you are trying to add null values'})

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_method_api(id):
    # When use sqlite, you must convert the int id for tuple
    conn = connect_to_bd()
    cursor = conn.cursor()
    # You can create a validation to check if the id exists in the database
    verify_id = cursor.execute("SELECT id FROM YourTable")
    check_id = id
    convert_to_tuple = (check_id,)
    if convert_to_tuple not in verify_id:
        return jsonify({'error':'This id not exist in the database'})
    else:
        cursor.execute(""" DELETE FROM YourTable WHERE id = ? """,(convert_to_tuple))
        conn.commit()
        conn.close()
        return jsonify({'sucess': 'This id is deleted'})
app.run()