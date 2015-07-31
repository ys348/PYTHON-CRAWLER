
import logging
import os
import cgi

from controllers import server
import webapp2
import jinja2


app = webapp2.WSGIApplication([
    ('/', server.MainHandler),
	('/urlgo/',server.UrlGoHandler),
	('/urlReTry/',server.UrlReGoHandler),
	('/urltracing/',server.UrlTrackingHandler),
	('/urlquery/',server.UrlQHandler)
], debug=True)


def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Oops! Naughty Mr. Jiggles (This is a 404)')
    response.set_status(404)

app.error_handlers[404] = handle_404