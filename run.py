from flask import Flask,g, redirect, url_for, session, request, jsonify
from flask import render_template
from flask_oauthlib.client import OAuth
from Driver import Driver
import json
import collections

app = Flask(__name__)
#app.debug = True
app.secret_key = 'development'

oauth = OAuth(app)
my_dr_global = Driver()

github = oauth.remote_app(
    'github',
    consumer_key='9668bff6a6d0cf60d387',
    consumer_secret='1adfdb0718d49e1f33bb68376ef439658c5f947d',
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

@github.tokengetter
def get_github_oauth_token():
    if 'github_token' in session:
        resp = session['github_token']
        return session.get('github_token')


@app.before_request
def before_request():
    g.user = None
    if 'github_token' in session:
        g.user = session['github_token']

@app.after_request
def remove_if_invalid(response):
    if "__invalidate__" in session:
        response.delete_cookie(app.session_cookie_name)
    return response

@app.route('/')
@app.route('/index')

def index():
    me = None
    if 'github_token' in session:
        me = json.loads(json.dumps(github.get('user').data), object_hook=_decode_dict)
        print(type(me))
    repos = None
    if 'repos' in session:
        repos = session["repos"]
    return render_template('index.html', me = me)


@app.route('/repos')

def repos():
    repos = None
    if 'repos' in session:
        repos = session["repos"]
    print(type(repos))
    return render_template('repos.html', repos = repos)


@app.route('/login')
def login():
    return github.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    print("inside authorized")
    resp = github.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session['github_token'] = (resp['access_token'], '')
    me = github.get('user')
    js = json.dumps(me.data)
    return redirect(url_for('index'))



# parse form data

@app.route('/getInputData', methods=['POST'])
def getInputData():
    username = request.form['username']
    methodName = request.form['radio']
    print(username)
    print(methodName)
    #result = my_dr_global.get_recommendations_for_username("tamil1", "USER_ITEM")
    result = my_dr_global.get_recommendations_for_username(username, methodName)
    repos = json.loads(result, object_hook=_decode_dict)
    session['repos'] = repos
    return redirect(url_for('repos'))

# for logged in user

@app.route('/make_recommendations')
def make_recommendations():
    me = (github.get('user').data)
    username = convert(me)['login']

    #result = my_dr_global.get_recommendations_for_username("tamil1", "USER_ITEM")
    result = my_dr_global.get_recommendations_for_username(username, "USER_ITEM")
    repos = json.loads(result, object_hook=_decode_dict)
    session['repos'] = repos
    return redirect(url_for('repos'))


if __name__ == "__main__":
    app.run()