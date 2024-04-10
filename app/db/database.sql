CREATE DATABASE ProjetGlo2005;
USE ProjetGlo2005;

CREATE TABLE Utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50),
    prenom VARCHAR(25),
    email VARCHAR(255) UNIQUE,
    age INT,
    pseudo VARCHAR(20) UNIQUE,
    mot_de_passe VARCHAR(255),
    photo_de_profil VARCHAR(255),
    bool_cuisinier BOOLEAN
);

CREATE TABLE Recette_ingredients (
	id_recette INT,
	id_ingredient INT,
	quantite FLOAT,
	PRIMARY KEY (id_ingredient)
);

CREATE TABLE Categorie_recettes(
	id INT PRIMARY KEY,
	type VARCHAR(100) UNIQUE
);

CREATE TABLE Type_recettes(
	id INT PRIMARY KEY,
	type VARCHAR(100) UNIQUE
);

CREATE TABLE Difficulte_recettes(
	id INT PRIMARY KEY,
	type VARCHAR(100) UNIQUE
);

CREATE TABLE Cuisinier_recettes(
	id_cuisinier INT,
	id_recette INT,
	PRIMARY KEY (id_cuisinier, id_recette)
);

CREATE TABLE Cuisiniers (
	id INT PRIMARY KEY,
	nombre_recette INTEGER,
	bio VARCHAR(255),
	photo_profil VARCHAR(2048),
	anne_experience tinyint,
	specialite INT ,
	FOREIGN KEY (id) REFERENCES Utilisateurs(id),
	FOREIGN KEY (specialite) REFERENCES Categorie_recettes(id)
);

CREATE TABLE Ingredients (
	id INT AUTO_INCREMENT PRIMARY KEY,
	nom VARCHAR(100)
);


CREATE TABLE Recettes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    temps_preparation ENUM('15', '30', '45', '60', '90', '120'),
    type_recette INT,
    categorie_recette INT,
    Portion ENUM('1', '2', '4', '8'),
    difficulte_recette INT,
    ingredient INT,
    photo VARCHAR(2048),
    etapes VARCHAR(2048),
    FOREIGN KEY (type_recette) REFERENCES Type_recettes(id),
    FOREIGN KEY (categorie_recette) REFERENCES Categorie_recettes(id),
    FOREIGN KEY (difficulte_recette) REFERENCES Difficulte_recettes(id),
    FOREIGN KEY (ingredient) REFERENCES Recette_ingredients (id_ingredient)
);


