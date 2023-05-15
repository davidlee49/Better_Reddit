import os
import json
from praw_reddit import *
from connect_local_db import *
from db_methods import *

# Specify the directory path
directory = r'C:\Users\ryu28\OneDrive\Desktop\Reddit Json Dump\2007'


def process_directory(directory):
    for filename in os.listdir(directory):
        item_path = os.path.join(directory, filename)

        if os.path.isfile(item_path):
            if filename != 'RS_2007-10':
                continue
            # Perform operations on the file
            process_file(item_path)

        # Recursively process the subdirectory
        elif os.path.isdir(item_path):
            print('Processing directory:', item_path)
            process_directory(item_path)

def process_file(item_path):
    # check if file has been previously processed
    last_line = 0
    with open('error_report.json', 'r') as file:
        last_update = json.load(file)
    # if item_path != last_update[-1]['file'] or last_update[-1]['completed'] is True:
    #     return
    # else:
    # last_line = last_update[-1]['last_line_added']

    # process the remaining data
    print('Processing file:', item_path)
    file = open(item_path)
    posts = []
    for line_num, line in enumerate(file):
        line = json.loads(line)
        if line_num < last_line:
            continue
        else:
            posts.append(f"t3_{line['id']}")

    praw_generator = praw_fetch_batch_post(posts)
    last_post_i = 0
    for post_i, post in enumerate(praw_generator):
        try:
            if post.created_utc < 1193064856:
                continue

            last_post_i = post_i
            # print(post.subreddit, post.id, post.score, post.permalink, post.title, post.thumbnail, post.created_utc)
            # print(type(str(post.subreddit)), type(post.id), type(post.created_utc))
            insert_row_v5(format_for_db(post))

        except Exception as e:
            print(str(e))
            log_event(item_path, False, post_i, str(e))
            # print("We ran into an error!: e")
            return

        # if post_i == 99:
        #     break


    log_event(item_path, True, last_post_i, 'None')
    print('Processing complete')




def format_for_db(post):
    json_blob = {
        'permalink': post.permalink,
        'title': post.title,
    }

    post_type = 0
    comment_count = 0
    # print((post.created_utc, post_type, post.score, comment_count, str(post.subreddit), post.id, post.author, json.dumps(json_blob)))
    return ((post.created_utc, post_type, post.score, comment_count, post.subreddit.display_name if post.subreddit else 'deleted', post.id, post.author.name if post.author else 'deleted',
            json.dumps(json_blob)))




def log_event(file_path, completion_status, cur_line, error=None):
    cur_file = os.path.basename(file_path)
    log_path = r"C:\Users\ryu28\PycharmProjects\BetterReddit\error_report.json"

    log_event = {
        'completed': completion_status,
        'last_line_added': cur_line,
        'error': error
    }

    with open(log_path, 'r') as log:
        log_json = json.load(log)

    if cur_file not in log_json:
        log_json[cur_file] = [log_event]
    else:
        log_json[cur_file].append(log_event)

    with open(log_path, 'w') as log:
        json.dump(log_json, log, indent=4)



process_directory(directory)


