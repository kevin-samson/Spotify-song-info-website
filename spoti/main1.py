from spoti import app
from flask import redirect, session, request, render_template
from spoti.forms import MainForm
import spotipy
import time
import json

CLI_ID = '44de3ff0881d48c8bf95d687e5c54980'
CLI_SEC = 'cb44c266456f483bb9efa4b092de9192'
REDIRECT_URI = 'http://127.0.0.1:5000/api_callback'
SCOPE = 'user-library-read'


@app.route("/verify")
def verify():
    # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id='44de3ff0881d48c8bf95d687e5c54980',
                                           client_secret='cb44c266456f483bb9efa4b092de9192',
                                           redirect_uri='http://127.0.0.1:5000/api_callback',
                                           scope='user-library-read')
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)


@app.route("/home", methods=['GET', 'POST'])
def index():
    form = MainForm()
    if form.validate_on_submit():
        url = form.website.data
        sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=CLI_ID, client_secret=CLI_SEC, redirect_uri=REDIRECT_URI,
                                               scope=SCOPE)
        token_info = sp_oauth.get_access_token()
        sp = spotipy.Spotify(auth=token_info)
        return sp.audio_analysis(url)
    return render_template('home.html', form=form)


# authorization-code-flow Step 2.
# Have your application request refresh and access tokens;
# Spotify returns access and refresh tokens
@app.route("/api_callback")
def api_callback():
    # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=CLI_ID, client_secret=CLI_SEC, redirect_uri=REDIRECT_URI,
                                           scope=SCOPE)
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code, check_cache=False)

    # Saving the access token along with all other token related info
    session["token_info"] = token_info

    return redirect("/")


# authorization-code-flow Step 3.
# Use the access token to access the Spotify Web API;
# Spotify returns requested data
@app.route("/go", methods=['GET', 'POST'])
def go():
    session['token_info'], authorized = get_token(session)
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    response = sp.current_user_playlists()

    print(json.dumps(response))

    return response


# Checks to see if token is valid and gets a new token if not
def get_token(session):
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
        sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=CLI_ID, client_secret=CLI_SEC, redirect_uri=REDIRECT_URI,
                                               scope=SCOPE)
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid
