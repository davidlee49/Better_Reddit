from flask import Flask, request
from flask_cors import CORS
from pushshift_api import *
from db_methods import show_post_from_date
from datetime import datetime

app = Flask(__name__)
CORS(app)


@app.route('/form', methods=['GET', 'POST'])
def index():

    data = request.form.to_dict()
    print(data)

    date_start = datetime.strptime(data['created_utc_start'], '%Y-%m-%d')
    date_start = int(date_start.timestamp())
    print(date_start)

    date_end = datetime.strptime(data['created_utc_end'], '%Y-%m-%d')
    date_end = int(date_end.timestamp())
    print(date_end)

    if date_end > 1236093580:
        posts = pushshift_api(date_end, date_start, data['subreddit'], data['title'])
        # print("returned posts from praw: ", posts)
        return posts
    else:
        posts = show_post_from_date(data['created_utc_start'], data['created_utc_end'], data['subreddit'])
        # print("returned posts from local sql: ", posts)
        return posts


if __name__ == '__main__':
    app.run(debug=True)