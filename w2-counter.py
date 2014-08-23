import webapp2
import uuid
from google.appengine.api import memcache
from google.appengine.api import mail

class UuidHandler(webapp2.RequestHandler):
    def get(self):
        uid = str(uuid.uuid4())
        memcache.set(uid, uid, 120)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(uid)

class MsgHandler(webapp2.RequestHandler):
    def post(self):
        # die UID validieren
        req_uid = self.request.get('uid')
        mem_uid = memcache.get(req_uid)
        if (mem_uid == req_uid):
            msg = self.request.get('msg')
            if (msg):
                msg = msg.strip()
                mail.send_mail(
                    sender = 'W2-Counter <do-not-reply@dirk-w2-counter.appspot.com>',
                    to = 'Dirk Dittmar <dirk.dittmar@test.va>',
                    subject = 'a message arrived...',
                    body = """someone send you a message:
<BEGIN>
%s
<END>
""" % msg
                )


application = webapp2.WSGIApplication([
    ('/app/uuid', UuidHandler),
    ('/app/msg', MsgHandler),
], debug=True)
