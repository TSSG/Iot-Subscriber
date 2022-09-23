from flask import Flask, request
from flask_restful import Api

app = Flask(__name__)
app.url_map.strict_slashes = False

if __name__ == '__main__':
    print("Storage manager started.")
    app.run(host="0.0.0.0", port=5007, debug=False)

