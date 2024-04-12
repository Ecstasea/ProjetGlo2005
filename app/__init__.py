from flask import Flask, render_template, request, redirect, url_for, session

import pymysql 

import os
from .db.database import Database

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db = Database(app)
    db.create_tables()
   # db.insert_fake_users()

   
    @app.route('/')
    def home():
        return redirect(url_for('accueil'))

    @app.route('/accueil')
    def accueil():
        cursor = db.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT r.nom, r.photo, d.type AS difficulte "
            "FROM Recettes r "
            "JOIN Difficulte_recettes d ON r.difficultee_recette = d.id"
        )
        recettes = cursor.fetchall()
        cursor.close()
        return render_template('accueil.html', recettes=recettes)




    # Modifiez votre fonction login()
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            # Utilisez la connexion à la base de données pour créer le curseur
            cursor = db.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM utilisateurs WHERE email = %s AND mot_de_passe = %s', (email, password))
            user = cursor.fetchone()
            cursor.close()

            if user:
                session['user_id'] = user['id']
                return redirect(url_for('dashboard'))
            else:
                error = 'Identifiants invalides. Veuillez réessayer.'
                return render_template('login.html', error=error)
        else:
            return render_template('login.html')

    # Modifiez votre fonction register()
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            nom = request.form['nom']
            prenom = request.form['prenom']
            email = request.form['email']
            age = request.form['age']
            pseudo = request.form['pseudo']
            mot_de_passe = request.form['mot_de_passe']
            photo_de_profil = ''
            bool_cuisinier = request.form.get('bool_cuisinier', False)

            # Utilisez la connexion à la base de données pour créer le curseur
            cursor = db.connection.cursor()
            cursor.execute(
                'INSERT INTO Utilisateurs (nom, prenom, email, age, pseudo, mot_de_passe, photo_de_profil, bool_cuisinier) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (nom, prenom, email, age, pseudo, mot_de_passe, photo_de_profil, bool_cuisinier))
            cursor.close()

            return redirect(url_for('login'))
        else:
            return render_template('register.html')


    @app.route('/dashboard')
    def dashboard():
        if 'user_id' in session:
            user_id = session['user_id']
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM Utilisateurs WHERE id = %s', (user_id,))
            user = cursor.fetchone()
            cursor.close()
            if user:
                return render_template('dashboard.html', user=user)
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

    @app.route('/account')
    def account():
        return render_template('account.html')

    @app.route('/search', methods=['GET'])
    def search():
        query = request.args.get('query')
        # Code pour effectuer une recherche
        # Retourne les résultats de la recherche dans un modèle de page approprié
        return render_template('search_results.html', query=query)

    @app.route('/recipes')
    def recipes():
        # Code pour afficher la liste des recettes
        return render_template('recipes.html')

    @app.route('/create_recipe')
    def create_recipe():
            # Code pour afficher le formulaire de création de recette
            return render_template('create_recipe.html')


    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('login'))
    
    return app
