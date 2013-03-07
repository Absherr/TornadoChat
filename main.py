import json
import datetime
import tornado.ioloop
import tornado.web
import os

history = []

class NewMsgHandler(tornado.web.RequestHandler):
    def post(self):
        login = self.get_argument("login", None)
        date = str(datetime.datetime.now().strftime('%d-%h-%Y, %H:%m:%S'))
        msg = self.get_argument("msg", None)

        history.append((login,date,msg))
        self.write(json.dumps({"login":login,"date":date,"msg":msg}))

class GetListHandler(tornado.web.RequestHandler):
    def get(self):
        d = {}
        d['length']=len(history)
        for i in range(len(history)):
            d[i]={"login":history[i][0],"date":history[i][1],"msg":history[i][2]}
        self.write(json.dumps(d))

class ChatHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("chat.html")

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    )

application = tornado.web.Application([
    (r"/", ChatHandler),
    (r"/getList", GetListHandler),
    (r"/new", NewMsgHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "static"}),

    ],**settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()