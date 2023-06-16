from flask import Flask, request
from flask_cors import CORS
from db_methods import *

app = Flask(__name__)
CORS(app)


@app.route('/form', methods=['GET', 'POST'])
def index():
    data = request.get_json()
    print(data)

    return show_post_from_date(data['month'], data['year'], data['subreddit'])


if __name__ == '__main__':
    app.run(debug=True)