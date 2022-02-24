from flask import Flask
from rest import rest_temp

app = Flask(__name__)

app.register_blueprint(rest_temp)

if "__main__" == __name__:
    app.run(host="0.0.0.0", port=80)