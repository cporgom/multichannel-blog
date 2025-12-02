import os
import requests
from flask import Flask, render_template, redirect, session, request, url_for
from dotenv import load_dotenv
from models import db, User
from requests_oauthlib import OAuth2Session

# Cargar claves
load_dotenv('conf.env')

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

db.init_app(app)

# CONFIGURACIÓN GOOGLE
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_AUTH_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/userinfo.profile"
]

# CONFIGURACIÓN TWITCH
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
TWITCH_AUTH_BASE_URL = "https://id.twitch.tv/oauth2/authorize"
TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
TWITCH_SCOPES = ["user:read:follows"]

# --- RUTAS PRINCIPALES ---

@app.route('/')
def index():
    # Si ya hemos hecho login con alguno, vamos directos al feed
    if 'google_token' in session or 'twitch_token' in session:
        return redirect(url_for('feed'))
    return render_template('login.html')

@app.route('/feed')
def feed():
    # AQUÍ EN LA FASE 2 METEREMOS LA LÓGICA DE CARGAR VIDEOS REALES
    # De momento pasamos una lista vacía para ver el diseño
    feed_items = [] 
    return render_template('feed.html', feed_items=feed_items)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- GOOGLE ---

@app.route('/login/google')
def login_google():
    redirect_uri = os.getenv("REDIRECT_URI") + "/callback/google"
    google = OAuth2Session(GOOGLE_CLIENT_ID, scope=GOOGLE_SCOPES, redirect_uri=redirect_uri)
    authorization_url, state = google.authorization_url(GOOGLE_AUTH_BASE_URL)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/callback/google')
def callback_google():
    try:
        auth_response = request.url.replace("http://", "https://")
        redirect_uri = os.getenv("REDIRECT_URI") + "/callback/google"
        
        google = OAuth2Session(GOOGLE_CLIENT_ID, state=session['oauth_state'], redirect_uri=redirect_uri)
        token = google.fetch_token(GOOGLE_TOKEN_URL, client_secret=GOOGLE_CLIENT_SECRET, authorization_response=auth_response)
        
        user_data = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
        google_user_id = user_data['id']

        user = User.query.filter_by(google_id=google_user_id).first()
        if not user:
            user = User(google_id=google_user_id)
            db.session.add(user)
        
        user.google_access_token = token['access_token']
        if token.get('refresh_token'):
            user.google_refresh_token = token.get('refresh_token')
        db.session.commit()
        
        # Guardamos en sesión que estamos logueados
        session['google_token'] = token
        
        # REDIRECCIÓN AL FEED EN LUGAR DE TEXTO
        return redirect(url_for('feed'))
    except Exception as e:
        return f"❌ Error en Google: {e}"

# --- TWITCH ---

@app.route('/login/twitch')
def login_twitch():
    redirect_uri = os.getenv("REDIRECT_URI") + "/callback/twitch"
    twitch = OAuth2Session(TWITCH_CLIENT_ID, scope=TWITCH_SCOPES, redirect_uri=redirect_uri)
    authorization_url, state = twitch.authorization_url(TWITCH_AUTH_BASE_URL)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/callback/twitch')
def callback_twitch():
    try:
        auth_response = request.url.replace("http://", "https://")
        redirect_uri = os.getenv("REDIRECT_URI") + "/callback/twitch"
        twitch = OAuth2Session(TWITCH_CLIENT_ID, state=session['oauth_state'], redirect_uri=redirect_uri)
        token = twitch.fetch_token(TWITCH_TOKEN_URL, client_secret=TWITCH_CLIENT_SECRET, include_client_id=True, authorization_response=auth_response)

        twitch_headers = {'Client-ID': TWITCH_CLIENT_ID, 'Authorization': f"Bearer {token['access_token']}"}
        user_info = requests.get('https://api.twitch.tv/helix/users', headers=twitch_headers).json()
        twitch_user_id = user_info['data'][0]['id']

        user = User.query.filter_by(twitch_id=twitch_user_id).first()
        if not user:
            user = User(twitch_id=twitch_user_id)
            db.session.add(user)
        
        user.twitch_access_token = token['access_token']
        if token.get('refresh_token'):
            user.twitch_refresh_token = token.get('refresh_token')
        db.session.commit()

        session['twitch_token'] = token
        
        # REDIRECCIÓN AL FEED EN LUGAR DE TEXTO
        return redirect(url_for('feed'))
    except Exception as e:
        return f"❌ Error en Twitch: {e}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, ssl_context='adhoc')