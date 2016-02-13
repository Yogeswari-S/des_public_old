""" Main application for public release"""
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.log
import Settings
import jira_ticket
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    """
    Class that handle most of the request, all the rest og the handling is done
    by page.js
    """
    @tornado.web.asynchronous
    def get(self):
        self.render('index.html')

class HelpHandler(tornado.web.RequestHandler):
    """
    This class is special as it also include a post request to
    deal with the form submission
    """
    @tornado.web.asynchronous
    def get(self):
        self.render('index.html')
    @tornado.web.asynchronous
    def post(self):
        name = self.get_argument("name", "")
        last = self.get_argument("lastname", "")
        email = self.get_argument("email", "")
        subject = self.get_argument("subject", "")
        question = self.get_argument("question", "")
        topic = self.get_argument("topic", "")
        topics = topic.replace(',','\n')
        jira_ticket.create_ticket(name, last, email, topics, subject, question)
        self.set_status(200)
        self.flush()
        self.finish()

class My404Handler(tornado.web.RequestHandler):
    """
    Handles 404 requests, basically bust just changin the status to 404
    """
    def get(self):
        self.set_status(404)
        self.render('index.html')
    def post(self):
        self.set_status(404)
        self.render('index.html')

class Application(tornado.web.Application):
    """
    The tornado application  class
    """
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/releases/sva1/help", HelpHandler),
            (r"/releases/sva1/content/(.*)", tornado.web.StaticFileHandler,\
            {'path':Settings.SVA1_PATH}),
            ]
        settings = {
            "template_path":Settings.TEMPLATE_PATH,
            "static_path":Settings.STATIC_PATH,
            "debug":Settings.DEBUG,
            "default_handler_class": My404Handler,
        }
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    """
    The main function
    """
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
