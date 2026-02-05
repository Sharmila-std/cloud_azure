from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# Connection String
CONNECTION_STRING = "mongodb+srv://sharmila:123456_sharmila@capstone.3xycmpu.mongodb.net/?appName=capstone"
client = MongoClient(CONNECTION_STRING)
db = client['cloud_azure']
students_collection = db['students'] # Changed to students collection

@app.route("/", methods=["GET"])
def index():
    search_query = request.args.get("search")
    if search_query:
        # Case-insensitive search for roll_number
        students = list(students_collection.find({"roll_number": {"$regex": search_query, "$options": "i"}}))
    else:
        students = list(students_collection.find())
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    roll_number = request.form["roll_number"]
    
    # Process subjects and marks
    # request.form.getlist returns a list of values for inputs with the same name
    subject_names = request.form.getlist("subject_names[]")
    subject_marks = request.form.getlist("subject_marks[]")
    
    subjects = []
    for s_name, s_mark in zip(subject_names, subject_marks):
        if s_name.strip() and s_mark.strip(): # Only add if both exist
            subjects.append({
                "name": s_name.strip(),
                "mark": int(s_mark)
            })

    student_data = {
        "name": name,
        "roll_number": roll_number,
        "subjects": subjects
    }
    
    students_collection.insert_one(student_data)
    return redirect("/")

@app.route("/edit/<id>")
def edit_student(id):
    student = students_collection.find_one({"_id": ObjectId(id)})
    return render_template("edit.html", student=student)

@app.route("/update/<id>", methods=["POST"])
def update_student(id):
    name = request.form["name"]
    roll_number = request.form["roll_number"]
    
    subject_names = request.form.getlist("subject_names[]")
    subject_marks = request.form.getlist("subject_marks[]")
    
    subjects = []
    for s_name, s_mark in zip(subject_names, subject_marks):
        if s_name.strip() and s_mark.strip():
            subjects.append({
                "name": s_name.strip(),
                "mark": int(s_mark)
            })

    updated_data = {
        "name": name,
        "roll_number": roll_number,
        "subjects": subjects
    }
    
    students_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
    return redirect("/")

@app.route("/delete/<id>")
def delete(id):
    students_collection.delete_one({"_id": ObjectId(id)})
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
