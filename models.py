from flask_sqlalchemy import SQLAlchemy

# Inicializamos la extensión de base de datos
db = SQLAlchemy()

# Definimos cómo es un "Usuario" en nuestra tabla
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Datos de Google
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    google_access_token = db.Column(db.String(200), nullable=True)
    google_refresh_token = db.Column(db.String(200), nullable=True)
    
    # Datos de Twitch
    twitch_id = db.Column(db.String(100), unique=True, nullable=True)
    twitch_access_token = db.Column(db.String(200), nullable=True)
    twitch_refresh_token = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<User {self.id}>'