from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
import mysql.connector
from mysql.connector import Error
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para la gestión de sesiones

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='userDB',
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
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
    # Verifica si el usuario ha iniciado sesión
    if 'username' in session:
        return send_from_directory('static', 'home.html')
    else:
        return redirect(url_for('index'))  # Redirige a la página de inicio si no está autenticado

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
    password = data['password'].encode('utf-8')

    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user and bcrypt.checkpw(password, user[2].encode('utf-8')):
        session['username'] = username  # Guarda el nombre de usuario en la sesión
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    else:
        return jsonify({"message": "Credenciales inválidas"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Elimina el nombre de usuario de la sesión
    return jsonify({"message": "Sesión cerrada exitosamente"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)