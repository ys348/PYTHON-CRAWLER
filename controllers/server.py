import os
import re
import logging
import json
import cgi
import time
import funcs
import sys
import webapp2
import jinja2
from gaesessions import get_current_session

from google.appengine.ext import ndb
from models.node import urlNode


class MainHandler(webapp2.RequestHandler):

	def get(self):
		session=get_current_session()
		firstName=session.get('firstName','')
		familyName=session.get('familyName','')
		message=session.get('message','')
		jinja_environment=self.jinja_environment
		template=jinja_environment.get_template('index.html')
		tpl_vars={"message":message,"firstName":firstName,"familyName":familyName}
		self.response.out.write(template.render(tpl_vars))
	
	def post(self):
		firstName=self.request.get("firstName",'')
		familyName=self.request.get("familyName",'')
		session=get_current_session()
		session['firstName']=firstName
		session['familyName']=familyName
		session['message']=''
		if len(firstName)<2 or len(familyName)<2:
			session['message']="First Name and Family Name are mandatory"
			self.redirect("/")


	@property
	def jinja_environment(self):
		jinja_environment = jinja2.Environment(
			loader=jinja2.FileSystemLoader(
				os.path.join(os.path.dirname(__file__),
						'../views'
				))
		)
		return jinja_environment

		


class UrlQHandler(webapp2.RequestHandler):
	def post(self):
		logging.info(self.request.body)
		data = json.loads(self.request.body)
    #    story = ndb.Key(Story, data['storyKey']).get()
    #    story.vote_count += 1
    #    story.put()
    #    self.response.out.write(json.dumps(({'story': story.to_dict()})))
		self.response.out.write(json.dumps(({'story': 'story'})))

	@property
	def jinja_environment(self):
		jinja_environment = jinja2.Environment(
			loader=jinja2.FileSystemLoader(
				os.path.join(os.path.dirname(__file__),
					'../views'
				))
		)
		return jinja_environment
		
global query_status
query_status=''
global query_termination
query_termination='N'

class UrlGoHandler(webapp2.RequestHandler):

	def post(self):
		#logging.info(self.request.body)
		request_url = self.request.get('url')
		crawler_mode= self.request.get('mode')
		query_status='pre-calculating... (in average, it takes 1 minute)'
		try:
			data=funcs.all_in_one_func(request_url,crawler_mode)
			if isinstance(data, dict):
				self.response.out.write(json.dumps(data))
			else :
				self.response.out.write(data)
		except Exception as ex:

			template = "An exception of type {0} occured. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			
			self.response.out.write(message)
			#exc_type, exc_obj, exc_tb = sys.exc_info()
			#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			#message=str(exc_type)+"  "+str(fname)+"  "+str(exc_tb.tb_lineno)
			#self.response.out.write(message)
			 
	@property
	def jinja_environment(self):
		jinja_environment = jinja2.Environment(
			loader=jinja2.FileSystemLoader(
				os.path.join(os.path.dirname(__file__),
					'../views'
				))
		)
		return jinja_environment
		

class UrlReGoHandler(webapp2.RequestHandler):

	def post(self):
		#logging.info(self.request.body)
		request_url = self.request.get('url')
		global query_termination
		query_termination='Y'
		time.sleep(1)
		global query_status
		query_status='terminating...'
		time.sleep(3)
		query_status=''
		#funcs.findAllUrl(request_url)
		self.response.out.write('terminating')
	
	@property
	def jinja_environment(self):
		jinja_environment = jinja2.Environment(
			loader=jinja2.FileSystemLoader(
				os.path.join(os.path.dirname(__file__),
					'../views'
				))
		)
		return jinja_environment
		
		
class UrlTrackingHandler(webapp2.RequestHandler):

	def post(self):
		global query_status
		self.response.out.write(query_status)
	
	
	@property
	def jinja_environment(self):
		jinja_environment = jinja2.Environment(
			loader=jinja2.FileSystemLoader(
				os.path.join(os.path.dirname(__file__),
					'../views'
				))
		)
		return jinja_environment
	