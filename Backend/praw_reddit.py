import praw
from env import praw_reddit_creds
import json
from db_methods import *

reddit = praw_reddit_creds()

url = '''
https://www.reddit.com/r/reddit.com/comments/60bpc/cyclops_comic/
'''
id = url.split('/')

def praw_fetch_batch_post(posts_list):
    problem_posts = []
    submissions = reddit.info(fullnames=posts_list[len(problem_posts):])
    # while len(problem_posts) != posts_list:
    #     try:
    #
    #     except Exception as e:
    #         print(str(e))
    #         problem_posts.append(posts_list[len(problem_posts)])


    # for count, sub in enumerate(submission2):
        # print(count, sub.title, sub.score, f'https://www.reddit.com{sub.permalink}')

    # for i in submissions:
    #     print('I FOUND IT')
    #     print(i.id, i.created_utc)

    return submissions

# praw_fetch_batch_post(['t3_60bpc'])

def praw_fetch_submission(postid):
    submission = reddit.submission(postid)
    post = submission

    # print(len(submission.comments))
    # print(submission.domain)



    json_blob = {
        'permalink': post.permalink,
        'title': post.title,
    }
    post_type = 0
    comment_count = 0
    insert_row_v5((post.created_utc, post_type, post.score, comment_count,
     post.subreddit.display_name if post.subreddit else 'deleted', post.id,
     post.author.name if post.author else 'deleted',
     json.dumps(json_blob)))



    post_type = 0
    comment_count = 0
    # print((post.created_utc, post_type, post.score, comment_count, post.subreddit.display_name, post.id, post.author.name if post.author else "none",))
    # print(submission.post_hint)
    # post_hint = submission.post_hint
    # post_hint = post_hint.split(':')
    # if post_hint[0] == 'image':
    #     print(submission.url)
    # elif post_hint[0] == 'link':
    #     print('fuck that its a link')
    # elif post_hint[0] == 'hosted':
    #     print(submission.media['reddit_video']['fallback_url'])
    # else:
    #     print(submission.secure_media_embed['media_domain_url'])

    # print(submission.title, submission.media['reddit_video']['fallback_url'])
    # print(submission.domain, submission.url, f'is this OC?: {submission.is_original_content}')


def fetch_top_posts(li):

    for submission in reddit.subreddit("confusingperspective").random_rising(limit=1):
        print(submission.url)
        return submission.url

    for submission in reddit.subreddit("redditdev+learnpython").top(time_filter="all", limit=5):
        print(submission.url)

    test = []
    fetched_vals = []
    for submission in reddit.subreddit("incremental_games").top(limit=10, time_filter="day"):
        test.append(f"https://www.reddit.com/r/{submission.subreddit}/comments/{submission}/")
        # print(submission.author, submission.clicked, submission.created_utc)
        fetched_vals.append((submission.name, str(submission.created_utc), submission.title))
        print(f"https://www.reddit.com/r/{submission.subreddit}/comments/{submission}/")


    print(test)
    # print(len(test))
    return fetched_vals

# fetch_top_posts([])
# praw_fetch_submission(f'{id[6]}')





