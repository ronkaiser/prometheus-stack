from flask import Flask
from random import randrange

app = Flask(__name__)

@app.route("/metrics", methods=["GET"])
def metrics():
    random = randrange(10)
    return "custom_metric" + " " + str(random)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')