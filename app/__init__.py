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

    from flask import render_template, request

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
        return render_template('accueil.html', recettes=recettes, cuisinier=cuisinier)

    @app.route('/categories')
    def categories():
        cursor = db.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Categorie_recettes")
        categories = cursor.fetchall()
        cursor.close()
        return render_template('categories.html', categories=categories)

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
                    cursor.execute('SELECT cr.id, cr.type FROM Cuisiniers c, categorie_recettes cr WHERE c.id = %s AND c.specialite = cr.id', (user_id,))
                    cat_cuisinier = cursor.fetchone()
                    cursor.execute('SELECT * FROM categorie_recettes')
                    categorie = cursor.fetchall()
                    cursor.close()
                    return render_template('account.html', user=user, cuisinier=cuisinier, categorie=categorie, cat_cuisinier=cat_cuisinier)
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

            # Vérifier si l'utilisateur est un cuisinier
            bool_cuisinier = request.form.get('bool_cuisinier', False)
            cursor = db.connection.cursor(pymysql.cursors.DictCursor)
            if bool_cuisinier:
                annee_experience = request.form.get('annee_experience', None)
                bio = request.form.get('bio', None)
                specialite = request.form.get('specialite', None)
                nouvelle_photo = request.files.get('nouvelle_photo', None)

                # Vérifier si une nouvelle photo a été téléchargée
                if nouvelle_photo.filename:
                    photo_path = os.path.join(app.static_folder, 'photos', nouvelle_photo.filename)
                    nouvelle_photo.save(photo_path)
                    chemin_relatif = "../static/photos/" + nouvelle_photo.filename
                    cursor.execute(
                    'UPDATE Cuisiniers SET annee_experience = %s, bio = %s, specialite = %s, photo_profil = %s WHERE id = %s',
                    (annee_experience, bio, specialite, chemin_relatif, user_id))
                else:
                    cursor.execute(
                    'UPDATE Cuisiniers SET annee_experience = %s, bio = %s, specialite = %s WHERE id = %s',
                    (annee_experience, bio, specialite, user_id))

            # Exécuter la requête SQL pour mettre à jour tous les attributs de l'utilisateur
            cursor.execute(
                'UPDATE utilisateurs SET nom = %s, prenom = %s, email = %s, age = %s, pseudo = %s, mot_de_passe = %s WHERE id = %s',
                (nom, prenom, email, age, pseudo, mot_de_passe, user_id))

                
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
                ingredients = request.form.getlist('ingredients')  # Liste des ID des ingrédients sélectionnés
                quantites = {}
                for ingredient_id in ingredients:
                    quantite = request.form.get(f'quantites[{ingredient_id}]')
                    quantites[ingredient_id] = quantite
                print("Ingrédients:", ingredients)
                print("Quantités:", quantites)  
                cursor = db.connection.cursor()
                cursor.execute("SELECT Max(id) + 1 AS next_id FROM Recettes")
                result = cursor.fetchone()
                new_id_recette = result['next_id']

                cursor.execute("INSERT INTO Cuisinier_recettes (id_cuisinier, id_recette) VALUES (%s, %s)", (user_id, new_id_recette))

                for ingredient_id, quantite in quantites.items():
                    print("new_id_recette:", new_id_recette)
                    print("ingredient_id:", ingredient_id)
                    print("quantite:", quantite)
                    cursor.execute("INSERT INTO Recette_ingredients (id_recette, id_ingredient, quantite) VALUES (%s, %s, %s)",
                                (new_id_recette, ingredient_id, quantite))

                cursor.execute("INSERT INTO Recettes (id, nom, temps_preparation, type_recette, categorie_recette, portion, difficultee_recette, photo, etapes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (new_id_recette, nom, temps_preparation, type_recette, categorie_recette, portion, difficulte_recette, chemin_relatif, etapes))
                db.connection.commit()  

                
                cursor.close()



                return redirect(url_for('accueil'))  # Rediriger vers la page d'accueil après la création de la recette
            else:
                return redirect(url_for('accueil'))
        else:
            cursor = db.connection.cursor()
            
            # Récupérer tous les ingrédients
            cursor.execute("SELECT * FROM ingredients")
            ingredients = cursor.fetchall()
            
            # Récupérer toutes les difficultés
            cursor.execute("SELECT * FROM difficulte_recettes")
            difficultes = cursor.fetchall()

            # Récupérer toutes les catégories de recettes
            cursor.execute("SELECT * FROM categorie_recettes")
            categories = cursor.fetchall()

            # Récupérer tous les types de recettes
            cursor.execute("SELECT * FROM type_recettes")
            types = cursor.fetchall()
            
            cursor.close()

            # Envoyer ces données au template pour les afficher dans les champs appropriés.
            return render_template('create_recipe.html', ingredients=ingredients, difficultes=difficultes, categories=categories, types=types)


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
