from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Flask is running on my Mac!</p>"