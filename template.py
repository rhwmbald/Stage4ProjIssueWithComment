import os
import cgi
import jinja2
import webapp2
from datetime import datetime
from google.appengine.ext import ndb

template_dir=os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class NotesPage(Handler):
	def get(self):
		self.render("notes.html")

class Post(ndb.Model):
  authors = ndb.StringProperty(indexed=True)
  contents = ndb.StringProperty(indexed=False)
  dates = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(Handler):
	def get(self):
		posts = Post.query().order(-Post.dates)
	    #for post in posts:
	    #	authors = cgi.escape(post.authors) 
	    #	contents = gi.escape(post.contents)
        self.render('mainPage.html', posts=posts)
        #self.render("mainPage.html", authors=authors, contents=contents)

	def post(self):
	    post=Post()
	    post.authors = self.request.get('authors')
	    post.contents = self.request.get('contents')
	    blank = Fasle
	    if post.authors.isspace():
	      self.render('error.html')
	    elif post.authors and post.contents: 
	      post.put()
	      import time
	      delay_time = .1
	      time.sleep(delay_time)
	      self.redirect('/')
	    else:
	      self.render('error.html')

class ErrorHandler(Handler):
    def get(self):
        self.render('error.html')

app = webapp2.WSGIApplication([('/', MainPage),
							   ('/error', ErrorHandler),
							   ('/notes', NotesPage),
							   ], 
								debug=True)
