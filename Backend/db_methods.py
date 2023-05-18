from env import *
import collections
import json
import time


connection = mysql_connector()
cursor = connection.cursor()


def insert_row_v5(data):
    insert_data_query = """
    INSERT INTO reddit_posts_v5 (date, subreddit, post_data)
    VALUES (%s, %s, %s)
    """

    # Execute the SQL query to insert the row
    cursor.execute(insert_data_query, data)

    # Commit the changes to the database
    connection.commit()


def create_table_v5():
    # NOTE: we are putting the majority of the post data into a JSON blob(score, url, and author)
    # NOTE: additionally, we are going to make the sub and date the primary key
    create_schema_query = """
    CREATE TABLE reddit_posts_v5 (
        date VARCHAR(255),
        subreddit VARCHAR(255),
        post_data JSON
    )
    """
# post_type INT, comment_count INT, score INT, post_id VARCHAR(10), author VARCHAR(50),
    # Execute the SQL query to create the schema
    cursor.execute(create_schema_query)

    # Commit the changes to the database
    connection.commit()

# create_table_v5()


def show_post_from_date(start, end, subreddit):
    start_time = time.time()
    cursor = connection.cursor()
    query = f'''
    SELECT *
    FROM reddit_posts_v5
    WHERE date >= '{start}' AND date <= '{end}' 
    '''

    if subreddit:
        query = query + f'AND subreddit = "{subreddit}"'

    cursor.execute(query)
    rows = cursor.fetchall()
    print(len(rows))
    count = collections.Counter()
    for row in rows:
        count[row[1]] += 1
    print(count)
    posts = []

    for post in rows:
        posts.extend(json.loads(post[2]))
        # print(posts)
    # print(posts)
    posts.sort(reverse=True, key=lambda post: post['score'])

    end_time = time.time()
    print(end_time-start_time)

    return posts[:50]

# show_post_from_date('2007-01-01', '2007-12-31', '')

def add_primary_key():
    cursor = connection.cursor()


    # Define the ALTER TABLE statement to add the primary key
    alter_statement = """
        ALTER TABLE reddit_posts_v5
        ADD PRIMARY KEY (date,subreddit)
    """

    # Execute the ALTER TABLE statement
    cursor.execute(alter_statement)

    # Commit the changes to the database
    connection.commit()

# add_primary_key()


def print_execution_plan(querry):
    cursor = connection.cursor()

    # Enable the query execution plan
    cursor.execute('''EXPLAIN SELECT * FROM reddit_posts_v5 
                    WHERE subreddit= 'reddit.com' ''')

    # Fetch and display the execution plan
    execution_plan = cursor.fetchall()
    for i, plan in enumerate(execution_plan):
        print_plan = zip(cursor.column_names, plan)
        print(list(print_plan))

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

print_execution_plan('test')