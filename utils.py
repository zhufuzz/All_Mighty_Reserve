from google.appengine.api import users

def checkUser(user, caller):

    if user:
        url = users.create_logout_url(caller.request.uri)
        url_linktext = 'Logout'
        return url, url_linktext
    else:
        url = users.create_login_url(caller.request.uri)
        url_linktext = 'Login'
        return url, url_linktext