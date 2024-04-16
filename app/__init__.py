import os

import pymysql
from flask import Flask, redirect, url_for, session, request, render_template
from pymysql import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from .db.database import Database


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db = Database(app)
    db.create_tables()

    @app.route('/')
    def home():
        session.pop('user_id',
                    None)  #Nous avons mis cette commande pour déconnecter l'utilisateur en cours en ouvrant la page d'accueil
        return redirect(url_for('accueil'))

    @app.route(
        '/accueil')  #Page d'accueil du site où tout est accessible depuis cette page (recettes, ingrédients, compte, catégories de recettes, barre de recherche)
    def accueil():
        cursor = db.connection.cursor(pymysql.cursors.DictCursor)  #Permet de se connecter à la bd local.
        search_query = request.args.get('ingredient')
        category_filter = request.args.get('category')
        user_id = session.get('user_id')
        cuisinier = False
        if user_id:
            cursor.execute("SELECT bool_cuisinier FROM Utilisateurs WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            if result and result['bool_cuisinier']:
                cuisinier = True

        if category_filter:
            cursor.execute(
                "SELECT r.nom, r.photo, d.type AS difficulte, r.id "
                "FROM Recettes r "
                "JOIN Difficulte_recettes d ON r.difficultee_recette = d.id "
                "JOIN Categorie_recettes cr ON r.categorie_recette = cr.id "
                "WHERE cr.type = %s", (category_filter,)
            )
        elif search_query:
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
        return render_template('accueil.html', recettes=recettes, cuisinier=cuisinier)

    @app.route('/categories')  #Permet de trouver des recettes selon une catégorie.
    def categories():
        cursor = db.connection.cursor(pymysql.cursors.DictCursor)
        user_id = session.get('user_id')
        cuisinier = False
        if user_id:
            cursor.execute("SELECT bool_cuisinier FROM Utilisateurs WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            if result and result['bool_cuisinier']:
                cuisinier = True
        cursor.execute("SELECT * FROM Categorie_recettes")
        categories = cursor.fetchall()
        cursor.close()
        return render_template('categories.html', categories=categories, cuisinier=cuisinier)

    @app.route('/search',
               methods=['POST'])  #Permet la recherche de recette sur la page d'accueil selon le titre de recette.
    def search():
        query = request.form.get('search_query')
        print("Received search query:", query)
        if not query:
            return render_template('search_results.html')

        cursor = db.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Ingredients WHERE nom LIKE %s", ('%' + query + '%',))
        ingredient_results = cursor.fetchall()

        cursor.execute("SELECT * FROM Recettes WHERE nom LIKE %s", ('%' + query + '%',))
        recipe_results = cursor.fetchall()
        cursor.close()

        return render_template('search_results.html', ingredient_results=ingredient_results,
                               recipe_results=recipe_results)

    @app.route('/recette/<int:id>')  #Permet l'affichage des recettes dans la base de donnée sur la page d'accueil.
    def recette(id):

        cursor = db.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT i.nom, ri.quantite FROM Ingredients i, Recette_ingredients ri WHERE ri.id_recette = %s AND ri.id_ingredient = i.id",
            (id,))
        ingredients = cursor.fetchall()

        cursor.execute(
            "SELECT r.nom, r.temps_preparation, r.portion, r.photo, r.etapes, dr.type as difficulte, tr.type as type, cat.type as categorie "
            "FROM Recettes r, Difficulte_recettes dr, Categorie_recettes cat, Type_recettes tr "
            "WHERE r.id = %s AND r.type_recette = tr.id AND r.categorie_recette = cat.id AND r.difficultee_recette = dr.id",
            (id,))
        recette = cursor.fetchone()

        cursor.execute("SELECT u.pseudo, c.photo_profil, c.id FROM Cuisinier_recettes cr, Cuisiniers c, Utilisateurs u "
                       "WHERE cr.id_recette = %s AND cr.id_cuisinier = c.id AND c.id = u.id", (id,))
        cuisinier = cursor.fetchone()
        cursor.close()

        return render_template('recette.html', ingredients=ingredients, recette=recette, cuisinier=cuisinier)

    @app.route('/login', methods=['GET', 'POST'])  #Permet de se connecter a son compte, la méthode vailde si le email et le mot de passe sont dans la bd.
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            cursor = db.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM utilisateurs WHERE email = %s', (email,))
            user = cursor.fetchone()
            cursor.close()

            if user and check_password_hash(user['mot_de_passe'], password):  #Permet le déchiffrage du mot de passe de la bd.
                session['user_id'] = user['id']
                session['pseudo'] = user['pseudo']
                return redirect(url_for('accueil'))
            else:
                error = 'Identifiants invalides. Veuillez réessayer.'
                return render_template('login.html', error=error)
        else:
            return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])  #Permet la création d'un compte. S'assure que les valeurs entreées sont valides et met à jour la table utilisateur.
    def register():
        if request.method == 'POST':
            nom = request.form['nom']
            prenom = request.form['prenom']
            email = request.form['email']
            age = request.form['age']
            pseudo = request.form['pseudo']
            mot_de_passe = generate_password_hash(
                request.form['mot_de_passe'])  #Permet le chiffrage d'un mot de passe avant de le mettre dans la bd.
            bool_cuisinier = request.form.get('bool_cuisinier', False)

            if not nom.isalpha():
                error = "Le nom ne doit contenir que des lettres."
                return render_template('register.html', error=error)

            if not prenom.isalpha():
                error = "Le prénom ne doit contenir que des lettres."
                return render_template('register.html', error=error)

            if not age.isdigit() or int(age) < 0:
                error = "L'âge doit être un nombre entier positif."
                return render_template('register.html', error=error)

            try:
                cursor = db.connection.cursor(pymysql.cursors.DictCursor)
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

    @app.route('/account')  #Permet la visualisation des informations du commpte et cuisnier.
    def account():
        if 'user_id' in session:
            user_id = session['user_id']
            cursor = db.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM utilisateurs WHERE id = %s', (user_id,))
            user = cursor.fetchone()
            cursor.close()

            if user:
                if user['bool_cuisinier']:
                    cursor = db.connection.cursor(pymysql.cursors.DictCursor)
                    cursor.execute('SELECT * FROM Cuisiniers WHERE id = %s', (user_id,))
                    cuisinier = cursor.fetchone()

                    cursor.execute(
                        'SELECT cr.id, cr.type FROM Cuisiniers c, categorie_recettes cr WHERE c.id = %s AND c.specialite = cr.id',
                        (user_id,))
                    cat_cuisinier = cursor.fetchone()

                    cursor.execute('SELECT * FROM categorie_recettes')
                    categorie = cursor.fetchall()
                    cursor.close()

                    return render_template('account.html', user=user, cuisinier=cuisinier, categorie=categorie,
                                           cat_cuisinier=cat_cuisinier)

                else:
                    return render_template('account.html', user=user)
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

    @app.route('/update_account',
               methods=['POST'])  #Permet la modificaton des informations du compte et le changement dans la bd.
    def update_account():
        if 'user_id' in session:
            user_id = session['user_id']
            nom = request.form['nom']
            prenom = request.form['prenom']
            email = request.form['email']
            age = request.form['age']
            pseudo = request.form['pseudo']
            mot_de_passe = generate_password_hash(request.form['mot_de_passe'])
            bool_cuisinier = request.form.get('bool_cuisinier', False)

            cursor = db.connection.cursor(pymysql.cursors.DictCursor)

            annee_experience = request.form.get('annee_experience', None)
            bio = request.form.get('bio', None)
            specialite = request.form.get('specialite', None)
            nouvelle_photo = request.files.get('nouvelle_photo', None)

            if nouvelle_photo.filename:
                photo_path = os.path.join(app.static_folder, 'photos', nouvelle_photo.filename)
                nouvelle_photo.save(photo_path)
                chemin_relatif = "../static/photos/" + nouvelle_photo.filename
                cursor.execute(
                    'UPDATE Cuisiniers SET annee_experience = %s, bio = %s, specialite = %s, photo_profil = %s WHERE id = %s',
                    (annee_experience, bio, specialite, chemin_relatif, user_id))
            else:
                cursor.execute('UPDATE Cuisiniers SET annee_experience = %s, bio = %s, specialite = %s WHERE id = %s',
                               (annee_experience, bio, specialite, user_id))

            cursor.execute(
                'UPDATE utilisateurs SET nom = %s, prenom = %s, email = %s, age = %s, pseudo = %s, mot_de_passe = %s WHERE id = %s',
                (nom, prenom, email, age, pseudo, mot_de_passe, user_id))

            db.connection.commit()
            cursor.close()

            return redirect(url_for('account'))
        else:
            return redirect(url_for('accueil'))

    @app.route('/create_recipe', methods=['GET', 'POST'])  #Permet la création d'une recette lorsque login et cuisinier.
    def create_recipe():
        if request.method == 'POST':
            if 'user_id' in session:
                user_id = session['user_id']
                nom = request.form['nom']
                temps_preparation = request.form['temps_preparation']
                type_recette = request.form['type_recette']
                categorie_recette = request.form['categorie_recette']
                portion = request.form['portion']
                difficulte_recette = request.form['difficulte_recette']
                photo = request.files['photo']
                photo_path = os.path.join(app.static_folder, 'photos', photo.filename)
                photo.save(photo_path)
                chemin_relatif = "../static/photos/" + photo.filename
                etapes = request.form['etapes']
                ingredients = request.form.getlist('ingredients')
                quantites = {}
                for ingredient_id in ingredients:
                    quantite = request.form.get(f'quantites[{ingredient_id}]')
                    quantites[ingredient_id] = quantite

                cursor = db.connection.cursor(pymysql.cursors.DictCursor)
                cursor.execute("SELECT MAX(id) + 1 AS next_id FROM Recettes")
                result = cursor.fetchone()
                new_id_recette = result['next_id']

                cursor.execute(
                    "INSERT INTO Recettes (id, nom, temps_preparation, type_recette, categorie_recette, portion, difficultee_recette, photo, etapes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (new_id_recette, nom, temps_preparation, type_recette, categorie_recette, portion,
                     difficulte_recette, chemin_relatif, etapes))

                cursor.execute("INSERT INTO Cuisinier_recettes (id_cuisinier, id_recette) VALUES (%s, %s)",
                               (user_id, new_id_recette))

                for ingredient_id, quantite in quantites.items():
                    cursor.execute(
                        "INSERT INTO Recette_ingredients (id_recette, id_ingredient, quantite) VALUES (%s, %s, %s)",
                        (new_id_recette, ingredient_id, quantite))

                db.connection.commit()
                cursor.close()

                return redirect(url_for('accueil'))
            else:
                return redirect(url_for('accueil'))
        else:
            cursor = db.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM ingredients")
            ingredients = cursor.fetchall()

            cursor.execute("SELECT * FROM difficulte_recettes")
            difficultes = cursor.fetchall()

            cursor.execute("SELECT * FROM categorie_recettes")
            categories = cursor.fetchall()

            cursor.execute("SELECT * FROM type_recettes")
            types = cursor.fetchall()

            cursor.close()

            return render_template('create_recipe.html', ingredients=ingredients, difficultes=difficultes,
                                   categories=categories, types=types)

    @app.route(
        '/ingredients')  #Permet de voir la liste des ingrédients et de trouver des recettes selon l'ingrédient choisi.
    def show_ingredients():
        cursor = db.connection.cursor(pymysql.cursors.DictCursor)
        user_id = session.get('user_id')
        cuisinier = False
        if user_id:
            cursor.execute("SELECT bool_cuisinier FROM Utilisateurs WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            if result and result['bool_cuisinier']:
                cuisinier = True
        cursor.execute("SELECT nom FROM Ingredients ")
        ingredients = cursor.fetchall()
        cursor.close()
        return render_template('ingredients.html', ingredients=ingredients, cuisinier=cuisinier)

    @app.route(
        '/profil_cuisinier/<int:id>')  #Permet l'affichage du profil d'un cusinier en selectionnant une recette (le cuisinier qui a publié la recette).
    def profil_cuisinier(id):
        cursor = db.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT c.id, c.nombre_recette, c.bio, c.photo_profil, c.annee_experience, cr.type AS categorie, u.pseudo FROM Cuisiniers c "
            "JOIN categorie_recettes cr ON c.specialite = cr.id JOIN utilisateurs u ON c.id = u.id WHERE c.id = %s ", (id,))
        cuisinier = cursor.fetchone()

        cursor.execute("SELECT r.* FROM Recettes r JOIN Cuisinier_recettes cr ON r.id = cr.id_recette WHERE cr.id_cuisinier = %s ", (id,))
        recettes = cursor.fetchall()
        cursor.close()
        return render_template('profil_cuisinier.html', cuisinier=cuisinier, recettes=recettes)

    @app.route('/logout') #Permet de se déconnecter et de revenir à la page d'accueil.
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('accueil'))

    return app
