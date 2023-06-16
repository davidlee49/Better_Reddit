from env import *
import json
import calendar

connection = mysql_connector()
cursor = connection.cursor()


def create_table_v5():
    # NOTE: we are putting the majority of the post data into a JSON blob(score, url, and author)
    # NOTE: additionally, we are going to make the sub and date the primary key
    create_schema_query = """
    CREATE TABLE reddit_posts_v5 (
        date VARCHAR(255),
        time_range VARCHAR(10),
        subreddit VARCHAR(255),
        post_data JSON,
        PRIMARY KEY (date, time_range, subreddit)
    )
    """

    cursor.execute(create_schema_query)
    connection.commit()


def insert_row_v5(date, time_range, subreddit, post_data):
    insert_data_query = """
    INSERT INTO reddit_posts_v5 (date, time_range, subreddit, post_data)
    VALUES (%s, %s, %s, %s)
    """

    # Execute the SQL query to insert the row
    cursor.execute(insert_data_query, (date, time_range, subreddit, post_data))

    # Commit the changes to the database
    connection.commit()


def show_post_from_date(month, year, subreddit):
    cursor = connection.cursor()

    days_in_month = calendar.monthrange(int(year), int(month))[1]
    days = [year+"-"+month+'-'+str(day+1) for day in range(days_in_month)]
    weeks = [year+"-"+month+'-'+'week'+str(week) for week in range(4)]

    days = tuple(days)
    weeks = tuple(weeks)
    month =(f"('{year}-{month}')")

    time_range = ['days', 'weeks', 'month']
    times = [days, weeks, month]

    posts = {'days': [], 'weeks': [], 'month': []}
    for i in range(3):
        query = f'''
        SELECT *
        FROM reddit_posts_v5
        WHERE date IN {times[i]}
        AND subreddit = '{ subreddit }'
        '''

        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            posts[time_range[i]].append(json.loads(row[3]))

    return posts


