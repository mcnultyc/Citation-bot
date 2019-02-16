import praw
import re     
import sys
import spacy
import requests
import urllib.parse
from collections import defaultdict
from lxml import etree


def get_page_ids(search_terms, limit):
    params = {'action' : 'query', 'format' : 'json', 'list' : 'search', 'srlimit': str(limit)}
    url = 'https://en.wikipedia.org/w/api.php'
    page_ids = []
    for search_term in search_terms:
        url_term = urllib.parse.quote(search_term)
        params['srsearch'] = url_term
        response = requests.get(url, params)
        json = response.json()
        if 'error' not in json:
            pages = json['query']['search']
            for page in pages:
                page_ids.append(page['pageid'])
    return page_ids


def get_pages(search_terms, limit):
    params = {'action' : 'parse', 'format' : 'json'}
    url = 'https://en.wikipedia.org/w/api.php'
    page_ids = get_page_ids(search_terms, limit)
    pages = []
    for page_id in page_ids:
        params['pageid'] = page_id
        response = requests.get(url, params)
        json = response.json()
        if 'error' not in json:
            page = defaultdict()
            page['title'] = json['parse']['title']
            page['html'] = json['parse']['text']['*']
            page['pageid'] = json['parse']['pageid']
            pages.append(page)
    return pages


def get_references_table(root, parser):
    references_xpath = '//ol[@class="references"]/li'
    references = root.xpath(references_xpath)
    citations_table = defaultdict(list)
    for citation in references:
        if 'id' in citation.attrib:
            cite_note = citation.attrib['id']
            for descendant in citation.iterdescendants(tag='a'):
                if 'class' in descendant.attrib:
                    if 'external' in descendant.attrib['class']:
                        link = descendant.attrib['href']
                        citations_table[cite_note].append(link)
    return citations_table
        

def print_reference_tables(search_terms, limit = 1):
    parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
    pages = get_pages(search_terms, limit)
    for page in pages:
        root = etree.fromstring(page['html'], parser)
        references_table = get_references_table(root, parser)
        count = 1
        for cite_note, references in references_table.items():
            print('{}. {}'.format(count, cite_note))
            for reference in references:
                print('\t', reference)
            count += 1


def print_citations(search_terms):
    parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
    citations_xpath = '//sup[@class="reference"]/a'
    pages = get_pages(search_terms, limit=10)
    for page in pages:
        html_tree = etree.fromstring(page['html'], parser)
        print(page['title'])
        citations = html_tree.xpath(citations_xpath)
        for i in range(0, len(citations)):
            print(i + 1, ':', citations[i].attrib['href'])
       

def print_references(search_terms):
    parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
    external_references_xpath = '//ol[@class="references"]//a[starts-with(@class, "external")]'
    pages = get_pages(search_terms, limit=10)
    for page in pages:
        html_tree = etree.fromstring(page['html'], parser)
        print('\n', page['title'], '\n')
        references = html_tree.xpath(external_references_xpath)
        for i in range(0, len(references)):
            print(i + 1, ':', references[i].text)


# This function splits a document by the inline
# citations used and creates a table using the
# cite note and preceding text.
# ex.
# <p>
#   Bill Clinton's father, 
#   <a title="William Jefferson Blythe Jr." href="/wiki/William_Jefferson_Blythe_Jr.">
#       William Jefferson Blythe Jr.
#   </a> 
#   (February 27, 1918 – May 17, 1946), was a traveling heavy equipment salesman who died 
#   in a car crash three months before Bill was born.
#   <sup class="reference" id="cite_ref-whitehouse.gov_bio_2-0">
#       <a href="#cite_note-whitehouse.gov_bio-2">[2]</a>
#   </sup> 
#   ...
# </p>
# citation table = { 
#    "#cite_note-whitehouse.gov_bio-2" :
#    "Bill Clinton's father, William Jefferson Blythe Jr. (February 27, 1918 – May 17, 1946)
#    , was a traveling heavy equipment salesman who died in a car crash three months 
#    before Bill was born."
#    }               
#
def get_citation_table(root):
    citation_table = defaultdict()
    # Iterate through paragraph elements
    for paragraph in root.iter('p'):
        text = paragraph.text if paragraph.text else ''
        # Iterate through descendants of paragraphs
        for elem in paragraph.iterdescendants(tag=etree.Element):
            if elem.get('class') != 'reference':
                parent = elem.getparent()
                # Check if elem is a nested citation
                if len(parent) and parent.get('class') == 'reference':
                    # Use cite note as key for text
                    citation_table[elem.get('href')] = text
                    # Check if parent reference class has tail
                    if parent.tail:
                        text = parent.tail
                    else:
                        # Check for adjacent citations
                        next = parent.getnext()
                        if next is None or next.get('class') != 'reference':
                            text = ''
                else:
                    # Add text and tail
                    if elem.text:
                        text += elem.text
                    if elem.tail:
                        text += elem.tail
    return citation_table
            
    
def print_citation_table(search_terms, limit = 1):
    parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
    pages = get_pages(search_terms, limit)
    for page in pages:
        root = etree.fromstring(page['html'], parser)
        citation_table = get_citation_table(root)
        for cite_note, text in citation_table.items():
            print('\n{}'.format(cite_note))
            print('{}\n'.format(text))

            
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
    reddit = praw.Reddit()
    # Iterate through top-10 submissions in the subreddit
    for submission in reddit.subreddit(subreddit).hot(limit=10):
        # Get citations from submission
        citations = get_citations(nlp, submission)
        # Iterate through citations
        for (comment, citation) in citations:
            # Respond to citation request
            respond_citation(comment, citation)
