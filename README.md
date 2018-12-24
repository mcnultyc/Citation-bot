Reddit bot to provide automatic citations
<h2><a href="https://www.reddit.com/user/Citation-bot/">Reddit Citation-bot profile</a></h2>
<h1>Setup:</h1>
<h2>Python packages to install:</h2>
<ul>
  <li>
    <p>
       Install <a href="https://praw.readthedocs.io/en/latest/">PRAW: The Python Reddit API Wrapper</a></br>
       by entering `pip install praw` in the command line.
    </p>
  </li>
  <li>
    <p>
      Install <a href="https://spacy.io/">SpaCy: Industrial Strength Natural Language Processing</a></br>
      by entering <b>pip install spacy</b> in the command line. You'll also need to install the <a href="https://github.com/explosion/spacy-models/releases//tag/en_core_web_sm-2.0.0">english language model</a></br>
      used by the script. There are two ways to do this. You can run <b>spacy download en_core_web_sm</b> from the</br>
      command line or download the tar file yourself. If you download the model yourself then you'll need to point</br>
      the installation process to your model by entering <b>pip install /Users/you/en_core_web_sm-2.0.0.tar.gz</b></br> 
      in the command line.
    </p>
  </li>
  <li>
    <p>
      Install <a href="https://scrapy.org/">Scrapy: A Fast and Powerful Scraping and Web Crawling Framework</a><br>
      by entering <b>pip install scrapy</b> in the command line.
    </p>
  </li>
</ul>
<h2>Using the wikipedia spider:</h2>
<p>Inside of the main <b>wikiSpider</b> directory you'll want to enter the command: <b>scrapy crawl article</b>.</br>
This calls the spider by the name of </b>article</b>, which was defined on the line: <b>name = "article"</b></br> 
in <b>/wikiSpider/wikiSpider/spiders/WikiArticleSpider.py</b>. To create the Scrapy project <b>scrapy startproject</br>
wikiSpider</b> was run from the command line.</p>
