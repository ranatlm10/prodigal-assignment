from pymongo import MongoClient
from werkzeug.routing import ValidationError

from exceptions.custom_exception import CustomException


class StudentService:

    def __init__(self):
        client = MongoClient('mongodb+srv://prodigal_be_test_01:prodigaltech@test-01-ateon.mongodb.net/sample_training')
        self.db = client.sample_training
        self.students_collection = self.db.students
        self.grades_collection = self.db.grades

    def get_student(self, student_id):
        if student_id is None:
            raise CustomException("Student id missing")

        student = self.students_collection.find_one({"_id": student_id})
        if student is None:
            raise CustomException("Student not found")

        return student

    def get_all_students(self):
        students = self.students_collection.find({})
        response = list(map(lambda x: {"student_id": x["_id"], "student_name": x["name"]}, list(students)))

        return {"result": response}

    def get_list_of_classes_for_student(self, student_id):
        student = self.get_student(student_id)

        class_list = list(self.grades_collection.distinct("class_id", {"student_id": student_id}))
        classes = list(map(lambda x: {"class_id": x}, class_list))

        return {"student_id": student_id, "student_name": student["name"], "classes": classes}

    def get_student_classwise_performance(self, student_id):
        student = self.get_student(student_id)

        scores = list(self.grades_collection.aggregate([{"$match": {"student_id": student_id}},
                                                        {"$project": {"class_id": 1, "_id": 0,
                                                                      "total_marks":
                                                                          {"$toInt": {"$sum": "$scores.score"}}}}]))

        return {"student_id": student_id, "student_name": student["name"], "classes": scores}

    def get_student_class_scores(self, student_id, class_id):
        self.get_student(student_id)

        if class_id is None:
            raise CustomException("Class id is missing")

        results = list(self.grades_collection.aggregate([{"$match": {"student_id": student_id, "class_id": class_id}},
                                                  {"$lookup": {"from": "students", "localField": "student_id",
                                                               "foreignField": "_id", "as": "student"}},
                                                  {"$unwind": {"path": "$student",
                                                               "preserveNullAndEmptyArrays": False}},
                                                  {"$project": {"class_id": 1, "student_id": "$student._id",
                                                                "student_name": "$student.name", "_id": 0,
                                                                "marks": "$scores",
                                                                "total_marks":
                                                                    {"$toInt": {"$sum": "$scores.score"}}}}]))

        if results is None:
            raise ValidationError("Score not found")

        result = results[0]
        for score in result['marks']:
            score['marks'] = int(score['score'])
            del score['score']

        result['marks'].append({"type": "total", "score": result['total_marks']})
        del result['total_marks']

        return result

    @staticmethod
    def func_Q1(db):
        grades_collection = db.grades
        student_list = list(grades_collection.distinct("student_id", {}))

        return len(student_list)
