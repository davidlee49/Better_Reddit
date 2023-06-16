from env import praw_reddit_creds


reddit = praw_reddit_creds()

url = '''
https://www.reddit.com/r/reddit.com/comments
'''
id = url.split('/')


def praw_fetch_batch_post(posts_list):
    problem_posts = []
    submissions = reddit.info(fullnames=posts_list[len(problem_posts):])

    return submissions


def praw_fetch_submission(postid):
    submission = reddit.submission(postid)
    post = submission
    return post









