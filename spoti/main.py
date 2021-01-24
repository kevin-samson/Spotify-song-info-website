import os
import time

import spotipy
import spotipy.exceptions
from flask import redirect, session, request, render_template, url_for, flash

from spoti import app
from spoti.forms import MainForm

CLI_ID = os.environ['CLI_ID'] #change this
CLI_SEC = os.environ['CLI_SEC'] # and this
SCOPE = 'user-library-read user-read-currently-playing user-read-playback-state'
REDIRECT_URI = 'https://spot-info.herokuapp.com/api_callback' # change this to 
 

@app.route('/')
def home():
    return render_template('welcome.html')


@app.route("/verify")
def verify():
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=CLI_ID, client_secret=CLI_SEC, redirect_uri=REDIRECT_URI,
                                           scope=SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)


@app.route("/api_callback")
def api_callback():
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=CLI_ID, client_secret=CLI_SEC, redirect_uri=REDIRECT_URI,
                                           scope=SCOPE)
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code, check_cache=False)

    session["token_info"] = token_info

    return redirect("index")


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
    if is_token_expired:
        sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=CLI_ID, client_secret=CLI_SEC, redirect_uri=REDIRECT_URI,
                                               scope=SCOPE)
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid


@app.route("/index", methods=['GET', 'POST'])
def index():
    form = MainForm()
    if form.validate_on_submit():
        url = form.website.data
        if 'https' in url:
            return redirect(url_for('go', url=os.path.basename(url).split("?")[0]))
        if form.submit2.data:
            return redirect(url_for('go', url='cur'))
        return redirect(url_for('go', url=url))
    return render_template("home.html", form=form)


@app.route("/song_info/<url>", methods=['GET', 'POST'])
def go(url):
    session['token_info'], authorized = get_token(session)
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    if url == 'cur':
        if sp.current_user_playing_track():
            track_data = sp.current_user_playing_track()['item']
            response = sp.audio_features([track_data['uri']])
            print(response)
        else:
            response = 'no track playing'
            track_data = None
    else:
        try:
            track_data = sp.track(url)
        except spotipy.exceptions.SpotifyException:
            flash('Enter valid data', 'danger')
            return redirect(url_for('index'))
        response = sp.audio_features([url])
        print(type(response[0]))
    if track_data:
        name = track_data['name']
        artist = ''.join([i['name'] + " " for i in track_data['album']['artists']])
        img = track_data['album']['images'][1]['url']
        return render_template('site.html', img=img, artist=artist, name=name, info=enumerate(response[0].items()))
    else:
        flash("No song playing")
        return redirect(url_for('index'))
