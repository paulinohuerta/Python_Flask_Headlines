# -*- coding: utf-8 -*-
from flask import Flask
import feedparser
from flask import render_template
from flask.views import MethodView
import json

app= Flask(__name__)

RSS_FEED = { 'elp':'http://ep00.epimg.net/rss/tags/ultimas_noticias.xml',
             'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'lav':'http://www.lavanguardia.com/mvc/feed/rss/politica',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'abc':'http://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml',
             'elm':'http://estaticos.elmundo.es/elmundo/rss/portada.xml'
}
Titles = {'elp':'El Pais: Ultimas noticas',
          'bbc':'BBC headlines',
          'lav':u'La Vanguardia: Política',
          'cnn':'CNN headlines',
          'abc':'ABC: Sevilla',
          'elm':'El Mundo'
}

articles = {}
articles['elp'] = feedparser.parse(RSS_FEED['elp'])['entries'][:5]
articles['bbc'] = feedparser.parse(RSS_FEED['bbc'])['entries'][:5]
articles['lav'] = feedparser.parse(RSS_FEED['lav'])['entries'][:5]
articles['cnn'] = feedparser.parse(RSS_FEED['cnn'])['entries'][:5]
articles['abc'] = feedparser.parse(RSS_FEED['abc'])['entries'][:5]
articles['elm'] = feedparser.parse(RSS_FEED['elm'])['entries'][:5]


def getting_unres(article):
       dict1 = {
              'title':article.title,
              'link':article.link,
              'published':article.published
       }
       if hasattr(article, 'summary'):
         dict1['summary'] = article.summary
       else:
         dict1['summary'] = ''
       return dict1


@app.route("/")
def get_news():
  return render_template("home.html", articles=articles,titles=Titles)

@app.route("/news/<string(length=3):journal>")
def get_one_journal(journal):
  if(journal not in articles):
     journal='elp'
  return render_template("home.html", one_journal=articles[journal],one_title=Titles[journal])

class NewView(MethodView) :
  def get(self, journal='elp', id=None):
     res = {}
     one_journal = []
     one_journal = articles[journal]
     res['journal']=journal
     if id is None:
        id=0;
        for article in one_journal:
            res[id] = getting_unres(article)
            id += 1
     else:
       article = one_journal[id]
       if not article:
         abort(404)
       res[id] = getting_unres(article)
     return json.dumps(res)

new_view = NewView.as_view('new_view')
app.add_url_rule('/api/news', view_func=new_view, methods=['GET'])
app.add_url_rule('/api/news/<string(length=3):journal>', view_func=new_view, methods=['GET'])
app.add_url_rule('/api/news/<string(minlength=3,maxlength=3):journal>/<int(min=0,max=4):id>', view_func=new_view, methods=['GET'])

                                                                   
if __name__ == '__main__':
  app.run(port=5300,debug=True)

