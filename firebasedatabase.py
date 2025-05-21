from flask import Flask, request, jsonify
import requests

Database = Flask(__name__)

FIREBASE_URL = "https://bandmanagementsystem-b2428-default-rtdb.asia-southeast1.firebasedatabase.app/"

@Database.route("/register", methods=["POST"])
def Register():
    Payload = request.get_json()
    username = Payload["Username"]
    password = Payload["Password"]

    # Check if user exists
    check = requests.get(f"{FIREBASE_URL}/users/{username}.json")
    if check.json() is not None:
        return jsonify({ "result": "This username already exists" }), 403

    # Save user
    response = requests.put(f"{FIREBASE_URL}/users/{username}.json", json={
        "Username": username,
        "Password": password
    })

    return jsonify({ "result": "A new account has been created" }), 200


@Database.route("/login", methods=["POST"])
def Login():
    Payload = request.get_json()
    username = Payload["Username"]
    password = Payload["Password"]

    # Get user
    user_response = requests.get(f"{FIREBASE_URL}/users/{username}.json")
    user_data = user_response.json()

    if user_data is None:
        return jsonify({ "result": "User not found" }), 404

    if user_data["Password"] == password:
        return jsonify({ "result": user_data }), 200
    else:
        return jsonify({ "result": "Invalid Password" }), 403


if __name__ == "__main__":
    Database.run(port=3000, debug=True)
