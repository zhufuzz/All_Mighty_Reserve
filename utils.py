from google.appengine.api import users

def checkUser(user, caller):
    if user:
        url = users.create_logout_url(caller.request.uri)
        url_linktext = 'Logout'
        return url, url_linktext
    else:
        url = users.create_login_url(caller.request.uri)
        url_linktext = 'Login'
        caller.redirect(url)
        return url, url_linktext
        # if users.get_current_user():
        # 	url = users.create_logout_url(self.request.uri)
        # 	url_linktext = 'Logout'
        # else:
        # 	url = users.create_login_url(self.request.uri)
        # 	url_linktext = 'Login'
        # 	self.redirect(users.create_login_url(self.request.uri))
        # user = users.get_current_user()