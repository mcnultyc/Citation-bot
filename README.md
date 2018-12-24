Reddit bot to provide automatic citations

## [Reddit Citation-bot profile](https://www.reddit.com/user/Citation-bot/)

# Setup:
## Python packages to install:
- Install [PRAW: The Python Reddit API Wrapper](https://praw.readthedocs.io/en/latest/)</br>
  by entering `pip install praw` in the command line.
  
- Install [SpaCy: Industrial Strength Natural Language Processing](https://spacy.io/)</br>
  by entering `pip install spacy` in the command line. You'll also need to install the [english language model](https://github.com/explosion/spacy-  models/releases//tag/en_core_web_sm-2.0.0)</br>
  used by the script. There are two ways to do this. You can run `spacy download en_core_web_sm` from the</br>
  command line or download the tar file yourself. If you download the model yourself then you'll need to point</br>
  the installation process to your model by entering `pip install /Users/you/en_core_web_sm-2.0.0.tar.gz`</br> 
  in the command line.
 
- Install [Scrapy: A Fast and Powerful Scraping and Web Crawling Framework](https://scrapy.org/)<br>
  by entering `pip install scrapy` in the command line.

## Using the wikipedia spider:
Inside of the main <b>wikiSpider</b> directory you'll want to enter the command: <b>scrapy crawl article</b>.</br>
This calls the spider by the name of </b>article</b>, which was defined on the line: <b>name = "article"</b></br> 
in <b>/wikiSpider/wikiSpider/spiders/WikiArticleSpider.py</b>. To create the Scrapy project <b>scrapy startproject</br>
wikiSpider</b> was run from the command line.
