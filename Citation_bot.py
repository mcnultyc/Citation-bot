import praw
import re     
import sys
import spacy
from collections import defaultdict

# Format citation response and reply to request
def respond_citation(comment, citation):
    # comment.reply(citation)
    # TODO
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

def extract_entity_relations(doc):
    # Merge noun phrases and entities into a single token
    spans = list(doc.ents) + list(doc.noun_chunks)
    for span in spans:
        span.merge()
    relations = []
    for token in doc:
        if token.dep_ in ('attr', 'dobj'):
            subject = [t for t in token.head.lefts if t.dep_ == 'nsubj']
            if subject:
                subject = subject[0]
                relations.append((subject, token))
        elif token.dep_ == 'pobj' and token.head.dep_ == 'prep':
            relations.append((token.head, token))
    return relations


# Handle citation request
def get_citation(nlp, comment_body):
    # Parse request
    doc = nlp(comment_body)
    sentences_ents = defaultdict()
    # Add entities for each sentence to dictionary
    for sentence in doc.sents:
        sentences_ents[sentence.orth_] = defaultdict(set)
        for entity in sentence.ents:
            sentences_ents[sentence.orth_][entity.label_].add(entity.text)
    # Add each noun chunk to sentences in dictionary
    for phrase in doc.noun_chunks:
        sentences_ents[phrase.sent.orth_][phrase.label_].add(phrase.text)
    if len(sentences_ents):
        return sentences_ents
    return None


# Get citations from submission
def get_citations(nlp, submission):
    # Remove MoreComments objects from comment forest
    submission.comments.replace_more(limit=0)
    # List of citation requests
    citations = []
    # Add top-level comments to stack
    comments_stack = submission.comments[:]
    # DFS through comment forest
    while comments_stack:
        # Get comment from top of stack
        comment = comments_stack.pop()
        if re.search('citation needed', comment.body, re.IGNORECASE):
            citation = get_citation(nlp, comment.body)
            # Test if citation could be created for original comment
            if citation is None:
                parent_comment = comment.parent
                if parent_comment != submission:
                    # Get citation from parent comment
                    citation = get_citation(nlp, parent_comment.body)
                    if citation:
                        citations.append((parent_comment, citation))
            else:
                # Add citation created for original comment
                citations.append((comment, citation))
        # Add comment replies to stack
        comments_stack.extend(comment.replies)
    return citations


if __name__ == '__main__':
    # Check for right number of arguments
    if len(sys.argv) < 2:
        print('Error missing argument. Usage: <subreddit>')
        sys.exit(-1)
    # Load english language model
    nlp = spacy.load('en_core_web_sm')
    # Get subreddit from command line
    subreddit = sys.argv[1]
    # Create reddit instance using our bots keys
    reddit = praw.Reddit(client_id='nqrfbiLMx2fN3w',
                     client_secret='9FIT26JP9cBlbD-hqEXBssLd2xs',
                     user_agent='Citation-bot')
    # Iterate through top-10 submissions in the subreddit
    for submission in reddit.subreddit(subreddit).hot(limit=10):
        # Get citations from submission
        citations = get_citations(nlp, submission)
        # Iterate through citations
        for (comment, citation) in citations:
            # Respond to citation request
            respond_citation(comment, citation)
