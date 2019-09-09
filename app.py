import json

from flask import Flask
from pymongo import MongoClient

from exceptions.custom_exception import CustomException
from services.student_service import StudentService
student_service = StudentService()

from services.class_service import ClassService
class_service = ClassService()

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.errorhandler(CustomException)
def global_exception_handler(error):
    return {"error_message": error.message}, error.status_code


@app.route("/students")
def get_all_students():
    return student_service.get_all_students()


@app.route("/student/<int:student_id>/classes")
def get_list_of_classes_for_student(student_id):
    return student_service.get_list_of_classes_for_student(student_id)


@app.route("/student/<int:student_id>/performance")
def get_student_classwise_performance(student_id):
    return student_service.get_student_classwise_performance(student_id)


@app.route("/classes")
def get_all_classes():
    return class_service.get_all_classes()


@app.route("/class/<int:class_id>/students")
def get_class_students(class_id):
    return class_service.get_all_class_students(class_id)


@app.route("/class/<int:class_id>/performance")
def get_class_studentwise_performance(class_id):
    return class_service.get_class_studentwise_performance(class_id)


@app.route("/class/<int:class_id>/final-grade-sheet")
def get_student_wise_gradesheet(class_id):
    return class_service.get_student_wise_gradesheet(class_id)


@app.route("/class/<int:class_id>/student/<int:student_id>")
@app.route("/student/<int:student_id>/class/<int:class_id>")
def get_student_class_scores(class_id, student_id):
    return student_service.get_student_class_scores(student_id, class_id)


@app.route("/q1")
def func_Q1():
    return json.dumps(StudentService.func_Q1(MongoClient('mongodb+srv://prodigal_be_test_01:prodigaltech@test-01-ateon.mongodb.net/sample_training').sample_training))


@app.route("/q2")
def func_Q2():
    return json.dumps(ClassService.func_Q2(MongoClient('mongodb+srv://prodigal_be_test_01:prodigaltech@test-01-ateon.mongodb.net/sample_training').sample_training))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
