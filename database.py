from flask import Flask, request, jsonify
import json
import os

Database = Flask(__name__)

# Ensure Users.json exists
if not os.path.exists("Users.json"):
    with open("Users.json", "w") as f:
        json.dump({}, f)

@Database.route("/register", methods=["POST"])
def Register():
    Payload = json.loads(request.get_data())

    NewUser = {
        "Username": Payload["Username"],
        "Password": Payload["Password"]
    }

    with open("Users.json", "r") as FileRead:
        Users = json.loads(FileRead.read())

    if Payload["Username"] in Users:
        return jsonify({
            "result": "This username already exists"
        }), 403

    Users[Payload["Username"]] = NewUser

    with open("Users.json", "w") as FileWrite:
        FileWrite.write(json.dumps(Users, indent=1))

    return jsonify({
        "result": "A new account has been created"
    }), 200

@Database.route("/login", methods=["POST"])
def Login():
    Payload = json.loads(request.get_data())

    with open("Users.json", "r") as FileRead:
        Users = json.loads(FileRead.read())

    if Payload["Username"] not in Users:
        return jsonify({
            "result": "User not found"
        }), 404

    User = Users[Payload["Username"]]

    if User["Password"] == Payload["Password"]:
        return jsonify({
            "result": User
        }), 200
    else:
        return jsonify({
            "result": "Invalid Password"
        }), 403

if __name__ == "__main__":
    Database.run(port=3000, debug=True)
