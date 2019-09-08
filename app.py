from flask import Flask
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient('mongodb+srv://prodigal_be_test_01:prodigaltech@test-01-ateon.mongodb.net/sample_training')


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
