from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["studentDB"]
collection = db["students"]

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dash():
    return render_template("dashboard.html")

@app.route("/students")
def get_students():
    data = []
    for s in collection.find():
        s["_id"] = str(s["_id"])
        data.append(s)
    return jsonify(data)
@app.route("/login", methods=["POST"])
def do_login():
    data = request.json

    if data["username"] == "admin" and data["password"] == "123":
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"fail"})

@app.route("/add", methods=["POST"])
def add_student():
    data = request.json
    collection.insert_one(data)
    return jsonify({"msg":"Student Added"})

@app.route("/delete/<id>", methods=["DELETE"])
def delete_student(id):
    collection.delete_one({"_id":ObjectId(id)})
    return jsonify({"msg":"Deleted"})

@app.route("/update/<id>", methods=["PUT"])
def update_student(id):
    data = request.json
    collection.update_one(
        {"_id":ObjectId(id)},
        {"$set":{
            "name":data["name"],
            "age":data["age"],
            "course":data["course"]
        }}
    )
    return jsonify({"msg":"Updated"})

if __name__ == "__main__":
    app.run(debug=True)