
import praw

from helpers import get_credentials

class RedditScraper():
    def __init__(self):
        creds = get_credentials()
        self.client_id = creds['client_id']
        self.client_password = creds['client_password']
        self.user_agent = creds['user_agent']
        self.create_reddit_instance()
        
    def create_reddit_instance(self):
        self.instance = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_password,
            user_agent=self.user_agent
        )
        
    def get_post(self, url):
        return self.instance.submission(url=url)
    
    def get_post_info(self, post):
        return post.title, post.author
    
    def get_post_comments(self, post):
        return [comment for comment in post.comments if comment.author == post.author]
    
    def get_review(self, comments):
        best_score = max([comment.score for comment in comments])
        return [comment for comment in comments if comment.score == best_score][0]
        
    
if __name__ == '__main__':        
    scrappy = RedditScraper()

    post = scrappy.get_post("https://www.reddit.com/r/bourbon/comments/10yvrfz/review_55_blantons_single_barrel_bourbon/")
    comments = scrappy.get_post_comments(post)

    print(comments)

    review = scrappy.get_review(comments)

    print(review.body)
        