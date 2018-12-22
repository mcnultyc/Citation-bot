import praw
import re     
import sys

# Handle citation request
def get_citation(request):
    # Entry point for parsing
    # TODO !!
    return None


# Format citation response and reply to request
def respond_citation(citation, request):
    # request.reply(citation)
    # TODO !!
    return

# Function to get the citation requests from a submission on reddit
def get_citation_requests(submission):
    # Remove MoreComments objects from comment forest
    submission.comments.replace_more(limit=0)
    requests = []
    # Iterate through comment forest
    for comment in submission.comments.list():
        # Search for 'citation needed' in body of comment
        if re.search('citation needed', comment.body, re.IGNORECASE):
            requests.append(comment)
    return requests

if __name__ == '__main__':
    # Check for right number of arguments
    if len(sys.argv) < 2:
        print('Error missing argument. Usage: <subreddit>')
        sys.exit(-1)
    # Get subreddit from command line
    subreddit = sys.argv[1]
    # Create reddit instance using our bots keys
    reddit = praw.Reddit(client_id='nqrfbiLMx2fN3w',
                     client_secret='9FIT26JP9cBlbD-hqEXBssLd2xs',
                     user_agent='Citation-bot')
    # Iterate through top-10 submissions in the subreddit
    for submission in reddit.subreddit(subreddit).hot(limit=10):
        # Get requests from submission
        requests = get_citation_requests(submission)
        # Handle any request
        if len(requests) == 0:
            print('No citation requests from submission "{0}"'.format(submission.title))
        else:
            for request in requests:
                # Get citation
                citation = get_citation(request)
                if citation is not None:
                    # Respond to request with citation
                    respond_citation(ccitation, request)