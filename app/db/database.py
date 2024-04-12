import pymysql

class Database:
    def __init__(self, app):
        self.connection = pymysql.connect(
            host=app.config['MYSQL_DATABASE_HOST'],
            port=int(app.config['MYSQL_DATABASE_PORT']),
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_DATABASE_PASSWORD'],
            db=app.config['MYSQL_DATABASE_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()

    def query(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def create_utilisateurs_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Utilisateurs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(50),
            prenom VARCHAR(25),
            email VARCHAR(255) UNIQUE,
            age INT,
            pseudo VARCHAR(20) UNIQUE,
            mot_de_passe VARCHAR(255),
            bool_cuisinier BOOLEAN
        )
        """
        self.cursor.execute(create_table_query)

    def create_recette_ingredients_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Recette_ingredients (
            id_recette INT,
            id_ingredient INT,
            quantite FLOAT,
            PRIMARY KEY (id_recette, id_ingredient),
            INDEX (id_ingredient)
        )
        """
        self.cursor.execute(create_table_query)

    def create_categorie_recettes_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Categorie_recettes (
            id INT PRIMARY KEY,
            type VARCHAR(100) UNIQUE
        )
        """
        self.cursor.execute(create_table_query)

    def create_type_recettes_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Type_recettes (
            id INT PRIMARY KEY,
            type VARCHAR(100) UNIQUE
        )
        """
        self.cursor.execute(create_table_query)

    def create_difficulte_recettes_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Difficulte_recettes (
            id INT PRIMARY KEY,
            type VARCHAR(100) UNIQUE
        )
        """
        self.cursor.execute(create_table_query)

    def create_cuisinier_recettes_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Cuisinier_recettes (
            id_cuisinier INT,
            id_recette INT,
            PRIMARY KEY (id_cuisinier, id_recette)
        )
        """
        self.cursor.execute(create_table_query)

    def create_cuisiniers_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Cuisiniers (
            id INT PRIMARY KEY,
            nombre_recette INTEGER,
            bio VARCHAR(255),
            photo_profil VARCHAR(2048),
            anne_experience tinyint,
            specialite INT ,
            FOREIGN KEY (id) REFERENCES Utilisateurs(id),
            FOREIGN KEY (specialite) REFERENCES Categorie_recettes(id)
        )
        """
        self.cursor.execute(create_table_query)

    def create_ingredients_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Ingredients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(100)
        )
        """
        self.cursor.execute(create_table_query)

    def create_recettes_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Recettes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(100),
            temps_preparation enum('15', '30', '45', '60', '90', '120'),
            type_recette INT,
            categorie_recette INT,
            Portion enum('1', '2', '4', '8'),
            difficultee_recette INT,
            ingredient INT,
            photo VARCHAR(2048),
            etapes VARCHAR(2048),
            FOREIGN KEY (type_recette) REFERENCES Type_recettes(id),
            FOREIGN KEY (categorie_recette) REFERENCES Categorie_recettes(id),
            FOREIGN KEY (difficultee_recette) REFERENCES Difficulte_recettes(id),
            FOREIGN KEY (ingredient) REFERENCES Recette_ingredients (id_recette)
        )
        """
        self.cursor.execute(create_table_query)

    def create_tables(self):
        self.create_utilisateurs_table()
        self.create_recette_ingredients_table()
        self.create_categorie_recettes_table()
        self.create_type_recettes_table()
        self.create_difficulte_recettes_table()
        self.create_cuisinier_recettes_table()
        self.create_cuisiniers_table()
        self.create_ingredients_table()
        self.create_recettes_table()
        self.connection.commit()

    def insert_fake_users(self):
        insert_users_query = """
        INSERT INTO Utilisateurs (nom, prenom, email, age, pseudo, mot_de_passe, photo_de_profil, bool_cuisinier)
        VALUES 
        ('Doe', 'John', 'john@example.com', 30, 'john_doe', 'mot_de_passe_1', 'photo1.jpg', TRUE),
        ('Smith', 'Jane', 'jane@example.com', 25, 'jane_smith', 'mot_de_passe_2', 'photo2.jpg', FALSE)
        """
        self.cursor.execute(insert_users_query)
        self.connection.commit()