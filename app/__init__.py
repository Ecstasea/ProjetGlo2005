from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
import pymysql
from werkzeug.security import generate_password_hash
import os
from .db.database import Database
from pymysql import IntegrityError


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
            "SELECT u.pseudo, c.photo_profil, c.id "
            "FROM Cuisinier_recettes cr, Cuisiniers c, Utilisateurs u "
            "WHERE cr.id_recette = %s AND cr.id_cuisinier = c.id AND c.id = u.id", (id,)
        )
        cuisinier = cursor.fetchone()
        cursor.close()

        return render_template('recette.html', ingredients=ingredients, recette=recette, cuisinier=cuisinier)

    # Modifiez votre fonction login()
    from werkzeug.security import check_password_hash

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            cursor = db.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM utilisateurs WHERE email = %s', (email,))
            user = cursor.fetchone()
            cursor.close()

            if user and check_password_hash(user['mot_de_passe'], password):
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
            # Chiffrer le mot de passe avant de l'ajouter à la base de données
            mot_de_passe = generate_password_hash(request.form['mot_de_passe'])
            bool_cuisinier = request.form.get('bool_cuisinier', False)

            try:
                # Utiliser la connexion à la base de données pour créer le curseur
                cursor = db.connection.cursor()
                cursor.execute(
                    'INSERT INTO Utilisateurs (nom, prenom, email, age, pseudo, mot_de_passe, bool_cuisinier) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (nom, prenom, email, age, pseudo, mot_de_passe, bool_cuisinier))
                db.connection.commit()
                cursor.close()
                return redirect(url_for('login'))
            except IntegrityError as e:
                error = "L'utilisateur avec cet email ou pseudo existe déjà."
                return render_template('register.html', error=error)
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

            if user:
                # Vérifier si l'utilisateur est un cuisinier
                if user['bool_cuisinier']:
                    cursor = db.connection.cursor(pymysql.cursors.DictCursor)
                    cursor.execute('SELECT * FROM Cuisiniers WHERE id = %s', (user_id,))
                    cuisinier = cursor.fetchone()
                    cursor.close()
                    return render_template('account.html', user=user, cuisinier=cuisinier)
                else:
                    return render_template('account.html', user=user)
            else:
                return redirect(url_for('login'))
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
            mot_de_passe = generate_password_hash(request.form['mot_de_passe'])
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

    @app.route('/create_recipe', methods=['GET', 'POST'])
    def create_recipe():
        if request.method == 'POST':
            #nom = request.form['nom']
            #type_recette = request.form['type_recette']
            #categorie_recette = request.form['categorie_recette']
            #portion = request.form['portion']
            #difficulte_recette = request.form['difficulte_recette']
            #ingredients = request.form.getlist('ingredients')
            #photo = request.files['photo']
            #etapes = request.form['etapes']

            # Traiter la photo (sauvegarde, etc.)
            #photo.save('../static/photos/food.png' + photo.filename)
            cursor = db.connection.cursor()

            cursor.execute("""
                    INSERT INTO Cuisinier_recettes(id_cuisinier, id_recette)
                VALUES (27, 24)
                                        """)
            db.connection.commit()
            cursor.close()

            cursor = db.connection.cursor()

            cursor.execute("""
                                INSERT INTO Recette_ingredients (id_recette, id_ingredient, quantite)
                                VALUES (24, 9, 150.0)
                            """)
            db.connection.commit()
            cursor.close()

            cursor = db.connection.cursor()

            cursor.execute("""
                    INSERT INTO Recettes (nom, temps_preparation, type_recette, categorie_recette, portion, difficultee_recette, photo, etapes)
                    VALUES ('sa', '15', 1, 1, '4', 1,'../static/photos/food.png', '')
                """)
            db.connection.commit()
            cursor.close()

            return redirect(url_for('accueil'))  # Rediriger vers la page d'accueil après la création de la recette
        else:
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

    @app.route('/profil_cuisinier/<int:id>')
    def profil_cuisinier(id):
        cursor = db.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT c.id, c.nombre_recette, c.bio, c.photo_profil, c.annee_experience, cr.type AS categorie, u.pseudo
            FROM Cuisiniers c
            JOIN categorie_recettes cr ON c.specialite = cr.id
            JOIN utilisateurs u ON c.id = u.id
            WHERE c.id = %s """, (id,)
        )
        cuisinier = cursor.fetchone()
        cursor.close()
        cursor = db.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT r.*
            FROM Recettes r
            JOIN Cuisinier_recettes cr ON r.id = cr.id_recette
            WHERE cr.id_cuisinier = %s """, (id,)
        )
        recettes = cursor.fetchall()
        cursor.close()
        return render_template('profil_cuisinier.html', cuisinier=cuisinier, recettes = recettes)

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('accueil'))

    return app
