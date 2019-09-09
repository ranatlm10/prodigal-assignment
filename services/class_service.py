import json

from pymongo import MongoClient

from exceptions.custom_exception import CustomException


class ClassService:

    def __init__(self):
        client = MongoClient('mongodb+srv://prodigal_be_test_01:prodigaltech@test-01-ateon.mongodb.net/sample_training')
        self.db = client.sample_training
        self.students_collection = self.db.students
        self.grades_collection = self.db.grades

    def get_all_classes(self):
        class_ids = set(self.grades_collection.distinct("class_id", {}))
        class_list = list(map(lambda x: {"class_id": x}, class_ids))

        return json.dumps(class_list)

    def get_all_class_students(self, class_id):
        if class_id is None:
            raise CustomException("Class id is missing")

        results = list(self.grades_collection.aggregate([{"$match": {"class_id": 0}},
                                                         {"$lookup": {"from": "students", "localField": "student_id",
                                                                      "foreignField": "_id", "as": "student"}},
                                                         {"$unwind": {"path": "$student",
                                                                      "preserveNullAndEmptyArrays": False}},
                                                         {"$project": {"student_id": "$student._id",
                                                                       "student_name": "$student.name", "_id": 0}}]))

        return {"class_id": class_id, "students": results}

    def get_class_studentwise_performance(self, class_id):
        if class_id is None:
            raise CustomException("Class id is missing")

        results = list(self.grades_collection.aggregate([{"$match": {"class_id": 0}},
                                                         {"$lookup": {"from": "students", "localField": "student_id",
                                                                      "foreignField": "_id", "as": "student"}},
                                                         {"$unwind": {"path": "$student",
                                                                      "preserveNullAndEmptyArrays": False}},
                                                         {"$project": {"student_id": "$student._id",
                                                                       "student_name": "$student.name", "_id": 0,
                                                                       "total_marks":
                                                                           {"$toInt": {"$sum": "$scores.score"}}}}]))

        return {"class_id": class_id, "students": results}

    def get_student_wise_gradesheet(self, class_id):
        if class_id is None:
            raise CustomException("Class id is missing")

        results = list(self.grades_collection.aggregate([{"$match": {"class_id": 0}},
                                                         {"$lookup": {"from": "students", "localField": "student_id",
                                                                      "foreignField": "_id", "as": "student"}},
                                                         {"$unwind": {"path": "$student",
                                                                      "preserveNullAndEmptyArrays": False}},
                                                         {"$project": {"student_id": "$student._id",
                                                                       "student_name": "$student.name", "_id": 0,
                                                                       "details": "$scores",
                                                                       "total_marks":
                                                                           {"$toInt": {"$sum": "$scores.score"}}}},
                                                         {"$sort": {"total_marks": -1}}]))

        count = len(results)

        for index, student in enumerate(results):
            for score in student['details']:
                score['marks'] = int(score['score'])
                del score['score']

            student['details'].append({"marks": student['total_marks'], "type": "total"})
            del student['total_marks']

            if index < count/12:
                student['grade'] = 'A'
            elif index < count/4:
                student['grade'] = 'B'
            elif index < count/2:
                student['grade'] = 'C'
            else:
                student['grade'] = 'D'

        return {"class_id": class_id, "students": results}

    @staticmethod
    def func_Q2(db):
        grades_collection = db.grades
        class_list = list(grades_collection.distinct("class_id", {}))

        return len(class_list)
