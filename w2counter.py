import os
import uuid
import webapp2
from webapp2_extras import sessions
from google.appengine.api import mail

class BaseHandler(webapp2.RequestHandler):

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

class UuidHandler(webapp2.RequestHandler):
    def get(self):
        uid = str(uuid.uuid4())
        self.session['uid'] = uid
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(uid)

class MsgHandler(webapp2.RequestHandler):
    def post(self):
        # die UID validieren
        req_uid = self.request.get('uid')
        mem_uid = self.session.get('uid')
        if (mem_uid == req_uid):
            msg = self.request.get('msg')
            if (msg):
                msg = msg.strip()
                mail.send_mail(
                    sender = 'W2-Counter <do-not-reply@dirk-w2-counter.appspotmail.com>',
                    to = 'Dirk Dittmar <papst@vatican.va>',
                    subject = 'a message arrived...',
                    body = msg
                )

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'CHANGE-THIS-BEFORE-DEPLOYMENT',
    'cookie_name': 'w2-counter-session'
}

debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

application = webapp2.WSGIApplication([
    ('/app/uuid', UuidHandler),
    ('/app/msg', MsgHandler),
], debug=debug, config=config)
