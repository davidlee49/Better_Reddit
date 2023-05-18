import os
from praw_reddit import *
from db_methods import *
from console_helper_methods import *

# Specify the directory path
directory = r'C:\Users\ryu28\OneDrive\Desktop\Reddit Json Dump\2007'


def process_directory(directory):
    for filename in os.listdir(directory):
        item_path = os.path.join(directory, filename)

        if os.path.isfile(item_path):
            # Perform operations on the file
            process_file(item_path)

        # Recursively process the subdirectory
        elif os.path.isdir(item_path):
            print('Processing directory:', item_path)
            process_directory(item_path)


def process_file(item_path):
    print('Processing file:', item_path)
    file = open(item_path)
    posts = []
    for line_num, line in enumerate(file):
        line = json.loads(line)
        # if line['created_utc'] < 1196467182:
        #     continue
        # else:
        posts.append(f"t3_{line['id']}")

    total_count, day_count, retry_count = 0, 0, 0
    cur_date = ''
    subreddit_posts_day = {}
    while total_count < len(posts):
        praw_generator = praw_fetch_batch_post(posts[total_count:])
        try:
            for post_i, post in enumerate(praw_generator):
                if not cur_date:
                    cur_date = get_date(post.created_utc)
                    update_subreddit_posts_day(post, subreddit_posts_day)
                elif cur_date != get_date(post.created_utc):
                    print(f'Successfully added {day_count} new submissions for subsmissions on {cur_date}, Total added: {total_count}')
                    update_top_for_all_subreddits(subreddit_posts_day)
                    save_to_db(cur_date, subreddit_posts_day)

                    cur_date = get_date(post.created_utc)
                    day_count = 0
                    subreddit_posts_day.clear()

                else:
                    update_subreddit_posts_day(post, subreddit_posts_day)


                # insert_row_v5(format_for_db(post))
                total_count += 1
                day_count += 1

        except Exception as e:
            retry_count += 1
            total_count += 5
            print(str(e), 'retry count: ', retry_count, 'total_count :', total_count)
            log_event(item_path, False, posts[total_count:total_count + 5], str(e))

        # if post_i == 99:
        #     break

    log_event(item_path, True, total_count, 'None')
    print('Processing complete')


def update_subreddit_posts_day(post, subreddits):
    subreddit = post.subreddit.display_name if post.subreddit else 'deleted'
    if subreddit in subreddits:
        subreddits[subreddit].append(post)
    else:
        subreddits[subreddit] = [post]

def update_top_for_all_subreddits(subreddits):
    #sort the list for all the subreddits, and then take only the top 50
    for subreddit in subreddits:
        subreddits[subreddit].sort(key=lambda post: post.score, reverse=True)
        subreddits[subreddit] = subreddits[subreddit][:50]


    return


def save_to_db(cur_day, subreddit_posts_day):
    for sub in subreddit_posts_day:
        json_blob = []
        for post in subreddit_posts_day[sub]:
            json_blob.append({
                'permalink': post.permalink,
                'title': post.title,
                'score': post.score,
                'id': post.id,
                'author': post.author.name if post.author else 'deleted'})
        insert_row_v5((cur_day, sub, json.dumps(json_blob)))


def format_for_db(post):
    json_blob = {
        'permalink': post.permalink,
        'title': post.title,
        'score': post.score,
        'id': post.id,
        'author': post.author.name if post.author else 'deleted'}

    post_type = 0
    comment_count = 0
    return post.created_utc, post.subreddit.display_name if post.subreddit else 'deleted', json.dumps(json_blob)


def log_event(file_path, completion_status, skipped_posts, error=None):
    cur_file = os.path.basename(file_path)
    log_path = r"C:\Users\ryu28\PycharmProjects\BetterReddit\error_report.json"

    log_event = {
        'completed': completion_status,
        'last_line_added': skipped_posts,
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


