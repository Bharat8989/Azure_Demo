from flask import Flask, jsonify 
from flask_cors import CORS 

app = Flask(__name__)
# CORS(app) 
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


@app.route('/')
def home():
    return "Welcome to the Flask App!"

@app.route('/about')
def about():
    return "This is the about page!"

@app.route('/user/<username>')
def user(username):
    return f"Hello, {username}!"


@app.route('/api/products')
def get_products():
    products_list = [
   
        {"id": 1, "name": "Laptop"},
        {"id": 2, "name": "Mobile"},
        {"id": 3, "name": "Headphones"}
    ]
    
    return jsonify(products_list) 


if __name__ == '__main__':
    app.run(debug=True)
