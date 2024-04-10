from flask import Flask, render_template
from .db.database import Database

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db = Database(app)
    db.create_tables()
   # db.insert_fake_users()

    @app.route('/')
    def display_login_page():
        #users = db.query("SELECT * FROM Utilisateurs")  # Récupérer les utilisateurs depuis la base de données
        #return render_template('login.html', users=users)
        return render_template('Accueil.html')

    return app
