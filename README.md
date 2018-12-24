# Citation-bot: bot to provide automatic citations

## :see_no_evil: [Reddit Citation-bot profile](https://www.reddit.com/user/Citation-bot/)

## :wrench: Setup
### Python packages to install
- Install [PRAW: The Python Reddit API Wrapper](https://praw.readthedocs.io/en/latest/)</br>
  by entering `pip install praw` in the command line. The API keys for the application are</br>
  available inside of the [Citation_bot.py](Citation_bot.py) script.
  
- Install [SpaCy: Industrial Strength Natural Language Processing](https://spacy.io/)</br>
  by entering `pip install spacy` in the command line. You'll also need to install the [english language model](https://github.com/explosion/spacy-models/releases//tag/en_core_web_sm-2.0.0)</br>
  used by the script. There are two ways to do this. You can run `spacy download en_core_web_sm` from the</br>
  command line or download the tar file yourself. If you download the model yourself then you'll need to point</br>
  the installation process to your model by entering `pip install /Users/you/en_core_web_sm-2.0.0.tar.gz`</br> 
  in the command line.
 
- Install [Scrapy: A Fast and Powerful Scraping and Web Crawling Framework](https://scrapy.org/)<br>
  by entering `pip install scrapy` in the command line.

### Using the wikipedia spider:
Inside of the main [wikiSpider](wikiSpider) directory you'll want to enter the command: `scrapy crawl article`.</br>
This calls the spider by the name of **article**, which was defined on the line: `name = "article"`</br> 
in [WikiArticleSpider](/wikiSpider/wikiSpider/spiders/WikiArticleSpider.py). To create the Scrapy project `scrapy startproject wikiSpider`</br>
was run from the command line.

## :book: Resources
- [API:Main page - MediaWiki](https://www.mediawiki.org/wiki/API:Main_page) - MediaWiki action API for Wikipedia.

- [ADAM - A Question Answering System](https://github.com/5hirish/adam_qas) - A question answering system that extracts answers</br>
  from Wikipedia to questions posed in natural language. It has some good examples on how to</br>
  [fetch and parse Wikipedia articles](https://github.com/5hirish/adam_qas/tree/master/qas/wiki) using the MediaWiki API.

- [XPath](https://en.wikipedia.org/wiki/XPath) - XPath is a markup pattern selector for XML-based documents (like HTML).</br>
  It combines the power of CSS selectors with the ability to traverse the [DOM](https://en.wikipedia.org/wiki/Document_Object_Model).</br>
  Microsoft has a great writeup on XPath with many [examples](https://msdn.microsoft.com/en-us/library/ms256086(v=vs.110).aspx) and there's
  a great </br> [cheatsheet](https://devhints.io/xpath) available online.
 
- [urllib](https://docs.python.org/3/library/urllib.html) - This is the built-in Python library for sending HTTP requests.

- [Natural Language Processing](https://en.wikipedia.org/wiki/Natural_language_processing)/[SpaCy](https://spacy.io/) - Wikipedia article on NLP, which might be helpful for understanding</br>
  SpaCy. This section on [major evaluations and tasks](https://en.wikipedia.org/wiki/Natural_language_processing#Major_evaluations_and_tasks) was particularly helpful. Here's an examples of</br>
  SpaCy's [dependency visualizer](https://spacy.io/usage/visualizers) in action.
