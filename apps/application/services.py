import json
import os


def load_questions():
    base_path = os.path.dirname(os.path.realpath(__file__))
    with open("{}/fixtures/questions.json".format(base_path), "r") as f:
        return json.loads(f.read())


def get_question(id):
    for question in load_questions():
        if question["id"] == id:
            return question
    else:
        return None
