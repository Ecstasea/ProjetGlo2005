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
        session.pop('user_id', None)  # Efface automatiquement 'user_id' de la session
        return redirect(url_for('accueil'))

    @app.route('/accueil')
    def accueil():
        cursor = db.connection.cursor(pymysql.cursors.DictCursor)
        search_query = request.args.get('ingredient')
        if search_query:
            cursor.execute(
                "SELECT r.nom, r.photo, d.type AS difficulte, r.id "
                "FROM Recettes r "
                "JOIN Difficulte_recettes d ON r.difficultee_recette = d.id "
                "JOIN Recette_ingredients ri ON r.id = ri.id_recette "
                "JOIN Ingredients i ON ri.id_ingredient = i.id "
                "WHERE i.nom = %s", (search_query,)
            )
        else:
            cursor.execute(
                "SELECT r.nom, r.photo, d.type AS difficulte, r.id "
                "FROM Recettes r "
                "JOIN Difficulte_recettes d ON r.difficultee_recette = d.id"
            )
        recettes = cursor.fetchall()
        cursor.close()
        return render_template('accueil.html', recettes=recettes)

    @app.route('/search', methods=['POST'])
    def search():
        query = request.form.get('search_query')
        print("Received search query:", query)  # Add this line for debugging
        if not query:
            return render_template('search_results.html')

        db = Database(app)
        cursor = db.connection.cursor()

        # Recherche des ingrédients
        cursor.execute("SELECT * FROM Ingredients WHERE nom LIKE %s", ('%' + query + '%',))
        ingredient_results = cursor.fetchall()

        # Recherche des recettes
        cursor.execute("SELECT * FROM Recettes WHERE nom LIKE %s", ('%' + query + '%',))
        recipe_results = cursor.fetchall()

        return render_template('search_results.html', ingredient_results=ingredient_results,
                               recipe_results=recipe_results)

    @app.route('/recette/<int:id>')
    def recette(id):
        # Recuperation des ingredients
        cursor = db.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT i.nom, ri.quantite "
            "FROM Ingredients i, Recette_ingredients ri "
            "WHERE ri.id_recette = %s AND ri.id_ingredient = i.id", (id,)
        )
        ingredients = cursor.fetchall()
        cursor.close()

        # Recuperation de la recette
        cursor = db.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT r.nom, r.temps_preparation, r.portion, r.photo, r.etapes, dr.type as difficulte, tr.type as type, cat.type as categorie "
            "FROM Recettes r, Difficulte_recettes dr, Categorie_recettes cat, Type_recettes tr "
            "WHERE r.id = %s AND r.type_recette = tr.id AND r.categorie_recette = cat.id AND r.difficultee_recette = "
            "dr.id",
            (id,)
        )
        recette = cursor.fetchone()
        cursor.close()

        # Recuperation du cuisinier
        cursor = db.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT u.pseudo, c.photo_profil "
            "FROM Cuisinier_recettes cr, Cuisiniers c, Utilisateurs u "
            "WHERE cr.id_recette = %s AND cr.id_cuisinier = c.id AND c.id = u.id", (id,)
        )
        cuisinier = cursor.fetchone()
        cursor.close()

        return render_template('recette.html', ingredients=ingredients, recette=recette, cuisinier=cuisinier)

    # Modifiez votre fonction login()
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            cursor = db.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM utilisateurs WHERE email = %s AND mot_de_passe = %s', (email, password))
            user = cursor.fetchone()
            cursor.close()

            if user:
                session['user_id'] = user['id']
                session['pseudo'] = user['pseudo']
                return redirect(url_for('accueil'))
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
            bool_cuisinier = request.form.get('bool_cuisinier', False)

            # Utilisez la connexion à la base de données pour créer le curseur
            cursor = db.connection.cursor()
            cursor.execute(
                'INSERT INTO Utilisateurs (nom, prenom, email, age, pseudo, mot_de_passe, bool_cuisinier) VALUES (%s, '
                '%s, %s, %s, %s, %s, %s)',
                (nom, prenom, email, age, pseudo, mot_de_passe, bool_cuisinier))
            db.connection.commit()
            cursor.close()

            return redirect(url_for('login'))
        else:
            return render_template('register.html')

    @app.route('/account')
    def account():
        if 'user_id' in session:
            user_id = session['user_id']
            cursor = db.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM utilisateurs WHERE id = %s', (user_id,))
            user = cursor.fetchone()
            cursor.close()
            return render_template('account.html', user=user)
        else:
            return redirect(url_for('login'))

    @app.route('/update_account', methods=['POST'])
    def update_account():
        if 'user_id' in session:
            user_id = session['user_id']

            # Récupérer toutes les valeurs des champs du formulaire
            nom = request.form['nom']
            prenom = request.form['prenom']
            email = request.form['email']
            age = request.form['age']
            pseudo = request.form['pseudo']
            mot_de_passe = request.form['mot_de_passe']
            bool_cuisinier = request.form.get('bool_cuisinier', False)

            cursor = db.connection.cursor()
            # Exécuter la requête SQL pour mettre à jour tous les attributs de l'utilisateur
            cursor.execute(
                'UPDATE utilisateurs SET nom = %s, prenom = %s, email = %s, age = %s, pseudo = %s, mot_de_passe = %s, bool_cuisinier = %s WHERE id = %s',
                (nom, prenom, email, age, pseudo, mot_de_passe, bool_cuisinier, user_id))

            db.connection.commit()
            cursor.close()
            return redirect(url_for('account'))
        else:
            return redirect(url_for('accueil'))

    @app.route('/recipes')
    def recipes():
        # Code pour afficher la liste des recettes
        return render_template('recipes.html')

    @app.route('/create_recipe')
    def create_recipe():
        # Code pour afficher le formulaire de création de recette
        return render_template('create_recipe.html')

    @app.route('/ingredients')
    def show_ingredients():
        cursor = db.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT nom "
            "FROM Ingredients ")
        ingredients = cursor.fetchall()
        cursor.close()
        return render_template('ingredients.html', ingredients=ingredients)

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('accueil'))

    return app
