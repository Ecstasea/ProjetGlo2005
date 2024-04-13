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
	annee_experience tinyint,
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
    difficultee_recette INT,
    ingredient INT,
    photo VARCHAR(2048),
    etapes VARCHAR(2048),
    FOREIGN KEY (type_recette) REFERENCES Type_recettes(id),
    FOREIGN KEY (categorie_recette) REFERENCES Categorie_recettes(id),
    FOREIGN KEY (difficultee_recette) REFERENCES Difficulte_recettes(id),
    FOREIGN KEY (ingredient) REFERENCES Recette_ingredients (id_recette)
);

-- Pour supprimer les tables dans l'odre sans conflit avec les clés
DROP TABLE IF EXISTS Recettes ;
DROP TABLE IF EXISTS Recette_ingredients ;
DROP TABLE IF EXISTS Cuisiniers ;
DROP TABLE IF EXISTS Categorie_recettes;
DROP TABLE IF EXISTS Type_recettes;
DROP TABLE IF EXISTS Difficulte_recettes;
DROP TABLE IF EXISTS Cuisinier_recettes;
DROP TABLE IF EXISTS Ingredients ;
DROP TABLE IF EXISTS Utilisateurs  ;

INSERT INTO Ingredients (nom) VALUES
('Sel'),
('Poivre'),
('Farine'),
('Oeufs'),
('Beurre'),
('Sucre'),
('Huile'),
('Lait'),
('Tomate'),
('Oignon'),
('chou vert'),
('Ail'),
('Pomme de terre'),
('Carotte'),
('Poulet'),
('Boeuf'),
('Porc'),
('Poisson'),
('Crevette'),
('Riz'),
('Pâtes'),
('Bouillon de poulet'),
('Bouillon de boeuf'),
('Vinaigre'),
('Moutarde'),
('Ketchup'),
('Mayonnaise'),
('Crème fraîche'),
('Fromage'),
('Pain'),
('Viande hachée'),
('Jambon'),
('Thon'),
('Saumon'),
('Morue'),
('pâte feuilletée'),
('Miel'),
("Sirop d'érable"),
('Chocolat'),
('Café'),
('Thé'),
('Rhum'),
('Vin rouge'),
('Bières'),
('Whisky'),
('Vodka'),
('Gin'),
('Tequila'),
('Ricard'),
('Martini'),
('Cointreau'),
('Triple sec'),
('Campari'),
('Baileys'),
('Cognac'),
('Armagnac'),
('Chartreuse'),
('Sambuca'),
('Limonecello'),
('Amaretto'),
('Curacao'),
('Grand Marnier'),
('Curaçao bleu'),
('Curaçao rouge'),
('Curacao vert'),
('Galliano'),
('Marasquin'),
('Midori'),
('Passoa'),
('Pernod'),
('Porto'),
('Pousse café'),
('Ratafia'),
('Sherry'),
('Southern Comfort'),
('Vermouth'),
('Curaçao blanc'),
('pâte à pizza'),
('sauce tomate'),
('mozzarella'),
('vin blanc'),
('champignons'),
('lardons'),
('biscuits à la cuillère'),
('mascarpone'),
('coq'),
('poivrons'),
('courgettes'),
('aubergines'),
('pâte brisée'),
('nori'),
('avocat'),
('concombre'),
('sauce soja'),
('nouilles ramen'),
('mirin'),
('gingembre'),
('légumes variés'),
('amandes'),
('vinaigre de riz'),
('fécule de maïs'),
('Pain à burger'),
('Viande haché'),
('Salade'),
('Tortillas'),
('Salsa'),
('Guacamole'),
('Citron vert'),
('Oignons rouges'),
('Olives'),
('Fromage feta'),
("Huile d'olive"),
('Vinaigre de vin rouge'),
('Origan'),
('Orange'),
('Citron jaune'),
('Pomme'),
('eau pétillante'),
('Chorizo'),
('Fruits de mer'),
('Petits pois'),
('Safran'),
('nouilles de riz'),
('germe de soja'),
('arachides hachées'),
('échalote'),
('sauce Pad Thai');

Select * from ingredients;

INSERT INTO Categorie_recettes (id, type) VALUES
(1, 'Mexicain'),
(2, 'Américain'),
(3, 'Japonais'),
(4, 'Italien'),
(5, 'Français'),
(6, 'Chinois'),
(7, 'Indien'),
(8, 'Thaïlandais'),
(9, 'Méditerranéen'),
(10, 'Grec'),
(11, 'Vietnamien'),
(12, 'Espagnol'),
(13, 'Brésilien'),
(14, 'Marocain'),
(15, 'Libanais'),
(16, 'Allemand'),
(17, 'Africain'),
(18, 'Portugais'),
(19, 'Russe'),
(20, 'Coréen');

Select * from Categorie_recettes;

INSERT INTO Type_recettes (id, type) VALUES
(1, 'Entrée'),
(2, 'Plat principal'),
(3, 'Dessert'),
(4, 'Goûter'),
(5, 'Boisson'),
(6, 'Apéritif'),
(7, 'Salade'),
(8, 'Soupes'),
(9, 'Végétarien'),
(10, 'Végétalien'),
(11, 'Sans gluten');

SELECT * FROM Type_recettes;

INSERT INTO Difficulte_recettes (id, type) VALUES
(1, 'Très facile'),
(2, 'Facile'),
(3, 'Moyen'),
(4, 'Difficile'),
(5, 'Très difficile');

Select * From Difficulte_recettes;

INSERT INTO Utilisateurs (nom, prenom, email, age, pseudo, mot_de_passe, bool_cuisinier) VALUES
('Dupont', 'Jean', 'jean.dupont@example.com', 30, 'jean.dupont', 'motdepasse1', TRUE),
('Martin', 'Marie', 'marie.martin@example.com', 15, 'marie.martin', 'motdepasse2',  FALSE),
('Dubois', 'Paul', 'paul.dubois@example.com', 28, 'paul.dubois', 'motdepasse3',  TRUE),
('Bernard', 'Sophie', 'sophie.bernard@example.com', 22, 'sophie.bernard', 'motdepasse4', TRUE),
('Lefevre', 'Pierre', 'pierre.lefevre@example.com', 35, 'pierre.lefevre', 'motdepasse5', FALSE),
('Robert', 'Catherine', 'catherine.robert@example.com', 27, 'catherine.robert', 'motdepasse6', TRUE),
('Petit', 'Thomas', 'thomas.petit@example.com', 29, 'thomas.petit', 'motdepasse7',  TRUE),
('Durand', 'Isabelle', 'isabelle.durand@example.com', 11, 'isabelle.durand', 'motdepasse8', FALSE),
('Leroy', 'Nicolas', 'nicolas.leroy@example.com', 26, 'nicolas.leroy', 'motdepasse9',  TRUE),
('Moreau', 'Sandrine', 'sandrine.moreau@example.com', 24, 'sandrine.moreau', 'motdepasse10', TRUE),
('Simon', 'David', 'david.simon@example.com', 33, 'david.simon', 'motdepasse11',  FALSE),
('Lefebvre', 'Laura', 'laura.lefebvre@example.com', 23, 'laura.lefebvre', 'motdepasse12',  TRUE),
('Michel', 'François', 'francois.michel@example.com', 32, 'francois.michel', 'motdepasse13',  TRUE),
('Garcia', 'Caroline', 'caroline.garcia@example.com', 29, 'caroline.garcia', 'motdepasse14',  TRUE),
('David', 'Éric', 'eric.david@example.com', 26, 'eric.david', 'motdepasse15',  FALSE),
('Martinez', 'Émilie', 'emilie.martinez@example.com', 30, 'emilie.martinez', 'motdepasse16', TRUE),
('Gauthier', 'Guillaume', 'guillaume.gauthier@example.com', 27, 'guillaume.gauthier', 'motdepasse17', TRUE),
('Aimarre', 'Jean', 'jean.aimarre@example.com', 28, 'jean.aimare', 'motdepasse18',  TRUE),
('Fournier', 'Mathieu', 'mathieu.fournier@example.com', 25, 'mathieu.fournier', 'motdepasse19',  FALSE),
('Lopez', 'James', 'james.lopez@example.com', 34, 'james.lopez', 'motdepasse20',  TRUE);

SELECT * FROM utilisateurs;

INSERT INTO Cuisiniers (id, nombre_recette, bio, photo_profil, annee_experience, specialite) VALUES
(1, 1, "Je suis passionné par la cuisine depuis mon enfance. J'ai travaillé dans plusieurs restaurants étoilés et je suis spécialisé dans la cuisine française.", '../static/photos/avatar_1.png', 10, 5),
(3, 1, "J'adore expérimenter de nouvelles recettes et découvrir de nouvelles saveurs. Ma spécialité est la cuisine asiatique, en particulier la cuisine japonaise.", '../static/photos/avatar_1.png', 7, 3),
(4, 1, "Je suis une cuisinière autodidacte avec une passion pour les recettes traditionnelles mexicaines. J'ai une expérience de 5 ans dans le domaine de la cuisine.", '../static/photos/avatar_1.png', 5, 1),
(6, 1, "Ma passion pour la cuisine m'a amené à voyager à travers le monde et à apprendre des techniques culinaires variées. Je me spécialisée dans la cuisine grecque.", '../static/photos/avatar_1.png', 15, 10),
(7, 3, "Je suis un amateur de cuisine depuis toujours, et j'ai décidé de faire de ma passion mon métier. Je me spécialise dans la cuisine italienne et j'adore partager mes recettes avec les autres.", '../static/photos/avatar_1.png', 8, 4),
(9, 2, "J'ai travaillé dans de nombreux restaurants étoilés et j'ai acquis une expérience précieuse dans le domaine de la cuisine. Je suis passionné par la cuisine française et je suis toujours à la recherche de nouvelles inspirations.", '../static/photos/avatar_1.png', 12, 5),
(10, 1, "Je suis une grande passionnée de cuisine depuis mon enfance. J'ai une expérience de 10 ans dans le domaine et je me spécialisée dans la cuisine asiatique, en particulier la cuisine chinoise.", '../static/photos/avatar_1.png', 10, 6),
(12, 2, "Je suis une cuisinierè passionnée avec une expérience de 8 ans dans le domaine de la cuisine. Ma spécialité est la cuisine espagnole et j'aime partager mes recettes avec les autres.", '../static/photos/avatar_1.png', 8, 12),
(13, 1, "J'ai grandi dans une famille où la cuisine était au centre de notre vie. J'ai appris les secrets de la cuisine italienne de ma grand-mère et j'ai développé ma propre passion pour la cuisine.", '../static/photos/avatar_1.png', 15, 4),
(14, 2, "Je suis une cuisinière autodidacte avec une passion pour la cuisine française. J'aime expérimenter de nouvelles recettes et découvrir de nouvelles saveurs.", '../static/photos/avatar_1.png', 6, 5),
(16, 1, "Je suis passionnée par la cuisine depuis mon enfance. J'ai acquis une expérience précieuse dans le domaine de la cuisine asiatique, en particulier la cuisine japonaise.", '../static/photos/avatar_1.png', 9, 3),
(17, 3, "Ma passion pour la cuisine m'a conduit à explorer diverses cultures culinaires à travers le monde. Je suis spécialisé dans la cuisine portugaise et j'aime partager mes recettes avec les autres.", '../static/photos/avatar_1.png', 10, 18),
(18, 1, "Je suis un grand amateur de cuisine depuis toujours. J'ai une passion pour la cuisine américaine et j'aime expérimenter de nouvelles recettes.", '../static/photos/avatar_1.png', 7, 2),
(20, 1, "Je suis passionné par la cuisine depuis mon enfance. J'ai une expérience de 6 ans dans le domaine et je me spécialise dans la cuisine asiatique, en particulier la cuisine thaïlandaise.", '../static/photos/avatar_1.png', 8, 8);

Select * From Cuisiniers;

INSERT INTO Recette_ingredients (id_recette, id_ingredient, quantite)
VALUES
(1, 35, 500), -- morue
(1, 13, 500), -- pommes de terre
(2, 13, 300), -- pommes de terre
(2, 11, 1),   -- chou vert
(3, 36, 1),   -- pâte feuilletée
(3, 8, 500), -- lait
(3, 28, 200), -- crème
(3, 6, 100), -- sucre
(3, 3, 50),  -- farine
(4, 78, 1),   -- pâte à pizza
(4, 79, 200), -- sauce tomate
(4, 80, 200), -- mozzarella
(5, 20, 300), -- riz arborio
(5, 81, 1),   -- vin blanc
(5, 82, 200), -- champignons
(6, 21, 400), -- spaghetti
(6, 83, 150), -- lardons
(6, 4, 2),   -- jaunes d'œufs
(7, 84, 250), -- biscuits à la cuillère
(7, 40, 200), -- café fort
(7, 85, 150), -- mascarpone
(8, 16, 800), -- viande de bœuf
(8, 43, 300), -- vin rouge
(8, 14, 500), -- carottes
(8, 82, 500), -- champignons
(9, 86, 1),   -- coq
(9, 43, 300), -- vin rouge
(9, 14, 500), -- carottes
(9, 82, 500), -- champignons
(10, 87, 4),   -- poivrons
(10, 88, 3),   -- courgettes
(10, 89, 2),   -- aubergines
(10, 9, 5),   -- tomates
(11, 90, 1),   -- pâte brisée
(11, 83, 200), -- lardons
(11, 4, 3),   -- œufs
(11, 28, 200), -- crème fraîche
(11, 29, 150), -- fromage râpé
(12, 10, 4),   -- oignons
(12, 5, 50),  -- beurre
(12, 3, 50),  -- farine
(12, 23, 1),   -- bouillon de bœuf
(12, 81, 100), -- vin blanc
(13, 20, 200), -- riz à sushi
(13, 91, 200), -- nori
(13, 34, 150), -- saumon
(13, 92, 100), -- avocat
(13, 93, 50),  -- concombre
(13, 14, 50),  -- carotte
(13, 94, 50),  -- sauce soja
(14, 95, 400), -- nouilles ramen
(14, 22, 300), -- bouillon de poulet
(14, 94, 50),  -- sauce soja
(14, 96, 30),  -- mirin
(14, 97, 10),  -- gingembre
(14, 4, 100), -- œufs
(14, 98, 100), -- légumes variés
(15, 15, 400), -- poulet
(15, 99, 100), -- amandes
(15, 94, 50),  -- sauce soja
(15, 100, 30),  -- vinaigre de riz
(15, 97, 20),  -- gingembre
(15, 12, 20),  -- ail
(15, 101, 50), -- fécule de maïs
(15, 6, 30), -- sucre
(16, 102, 1),  -- Pain à burger
(16, 103, 1),  -- Steak haché
(16, 29, 2),  -- Tranches de fromage
(16, 104, 1),  -- Laitue
(16, 9, 1),  -- Tomate
(16, 10, 1),  -- Oignon
(16, 26, 1),  -- Ketchup
(17, 105, 4),   -- Tortillas
(17, 103, 300), -- Viande hachée
(17, 106, 1),   -- Salsa
(17, 107, 1),   -- Guacamole
(17, 29, 100), -- Fromage râpé
(17, 108, 0.5), -- Citron vert
(18, 93, 1),  -- Concombres
(18, 9, 2),  -- Tomates
(18, 109, 0.5),-- Oignons rouges
(18, 110, 10), -- Olives kalamata
(18, 111, 100),-- Fromage feta
(18, 112, 2),  -- Huile d'olive
(18, 113, 1),  -- Vinaigre de vin rouge
(18, 114, 1),  -- Origan
(18, 1, null),-- Sel
(18, 2, null),-- Poivre
(19, 43, 1),   -- Vin rouge
(19, 115, 2),   -- Oranges
(19, 116, 2),   -- Citrons
(19, 117, 1),   -- Pommes
(19, 6, 50),  -- Sucre
(19, 52, 50),  -- Triple sec
(19, 71, 50),  -- Brandy = porto
(19, 118, 300), -- Eau pétillante
(20, 20, 1),   -- Riz à paella
(20, 15, 300), -- Poulet
(20, 119, 200), -- Chorizo
(20, 120, 200), -- Fruits de mer (moules, crevettes, calamars)
(20, 9, 2),   -- Tomates
(20, 87, 1),   -- Poivrons
(20, 121, 100), -- Petits pois
(20, 122, 0.5), -- Safran
(20, 22, 500), -- Bouillon de poulet
(21, 123, 200), -- nouilles de riz
(21, 19, 100), -- crevettes
(21, 4, 1),   -- œuf
(21, 124, 50),  -- germe de soja
(21, 125, 50),  -- arachides hachées
(21, 12, 1),   -- ail
(21, 126, 1),   -- échalote
(21, 127, 100); -- sauce Pad Thai

Select * From Recette_ingredients;

INSERT INTO Cuisinier_recettes (id_cuisinier, id_recette)
VALUES
(17, 1), -- Id du cuisinier qui a créé la recette Bacalhau à Brás
(17, 2), -- Id du cuisinier qui a créé la recette Caldo Verde
(17, 3), -- Id du cuisinier qui a créé la recette Pastéis de Nata
(7, 4), -- Id du cuisinier qui a créé la recette Pizza Margherita
(7, 5), -- Id du cuisinier qui a créé la recette Risotto aux champignons
(7, 6), -- Id du cuisinier qui a créé la recette Pasta Carbonara
(13, 7), -- Id du cuisinier qui a créé la recette Tiramisu
(1, 8), -- Id du cuisinier qui a créé la recette Boeuf bourguignon
(9, 9), -- Id du cuisinier qui a créé la recette Coq au vin
(9, 10), -- Id du cuisinier qui a créé la recette Ratatouille
(14, 11), -- Id du cuisinier qui a créé la recette Quiche Lorraine
(14, 12), -- Id du cuisinier qui a créé la recette Soupe à l'oignon
(3, 13), -- Id du cuisinier qui a créé la recette Sushi
(16, 14), -- Id du cuisinier qui a créé la recette Ramen
(10, 15), -- Id du cuisinier qui a créé la recette Poulet aux amandes
(18, 16), -- Id du cuisinier qui a créé la recette Burger américain
(4, 17), -- Id du cuisinier qui a créé la recette Tacos mexicains
(6, 18), -- Id du cuisinier qui a créé la recette Salade grecque
(12, 19), -- Id du cuisinier qui a créé la recette Sangria espagnole
(12, 20), -- Id du cuisinier qui a créé la recette Paella espagnole
(20, 21); -- Id du cuisinier qui a créé la recette pad Thaï

SELECT * FROM Cuisinier_recettes;

INSERT INTO Recettes (nom, temps_preparation, type_recette, categorie_recette, Portion, difficultee_recette, ingredient, photo, etapes)
VALUES
('Bacalhau à Brás', '45', 2, 18, '2', 3, 1, 'bacalhau_bras.jpg', "Étape 1: Faites cuire les pommes de terre dans de l\'eau bouillante salée jusqu\'à ce qu\'elles soient tendres. Égouttez et écrasez-les grossièrement. Étape 2: Dans une poêle, faites revenir l\'oignon et l\'ail dans de l\'huile d\'olive. Étape 3: Ajoutez le morue dessalée et émiettée et faites cuire jusqu\'à ce qu\'elle soit dorée. Étape 4: Ajoutez les pommes de terre écrasées et mélangez bien. Étape 5: Battez les œufs et versez-les sur le mélange de morue et de pommes de terre. Remuez jusqu'à ce que les œufs soient cuits. Servez chaud."),
('Caldo Verde', '30', 2, 18, '8', 2, 2, 'caldo_verde.jpg', "Étape 1: Faites bouillir de l\'eau dans une casserole et ajoutez les pommes de terre coupées en dés. Étape 2: Lorsque les pommes de terre sont tendres, écrasez-les grossièrement avec une fourchette. Étape 3: Ajoutez le chou vert coupé en fines lanières et laissez cuire jusqu'à ce qu'il soit tendre. Étape 4: Assaisonnez avec du sel et du poivre selon votre goût. Étape 5: Versez un filet d'huile d'olive et servez chaud."),
('Pastéis de Nata', '60', 3, 18, '4', 3, 3, 'pasteis_nata.jpg', "Étape 1: Préchauffez votre four à 220°C. Étape 2: Déroulez la pâte feuilletée et découpez-la en petits carrés. Étape 3: Disposez les carrés de pâte dans des moules à muffins en les pressant pour former des petits bols. Étape 4: Préparez la crème en mélangeant le lait, la crème, le sucre et la farine dans une casserole. Faites chauffer à feu moyen jusqu'à ce que le mélange épaississe. Étape 5: Versez la crème dans les bols de pâte et enfournez pendant 15 à 20 minutes, jusqu'à ce que la pâte soit dorée. Laissez refroidir avant de servir."),
('Pizza Margherita', '30', 2, 4, '4', 2, 4, 'pizza_margherita.jpg', "Étape 1: Préchauffez votre four à 220°C. Étape 2: Étalez la pâte à pizza sur une plaque de cuisson. Étape 3: Étalez la sauce tomate sur la pâte. Étape 4: Répartissez la mozzarella et les feuilles de basilic sur la sauce. Étape 5: Enfournez la pizza pendant 15 à 20 minutes, jusqu'à ce que la croûte soit dorée."),
('Risotto aux champignons', '45', 2, 4, '4', 3, 5, 'risotto_champignons.jpg', "Étape 1: Faites chauffer le bouillon de légumes dans une casserole. Étape 2: Dans une autre casserole, faites revenir l\'oignon dans du beurre jusqu\'à ce qu\'il soit translucide. Étape 3: Ajoutez le riz arborio et remuez jusqu'à ce qu'il devienne translucide. Étape 4: Ajoutez le vin blanc et laissez réduire. Étape 5: Ajoutez une louche de bouillon chaud au riz et remuez jusqu'à absorption. Continuez à ajouter du bouillon et à remuer jusqu'à ce que le riz soit cuit. Étape 6: Ajoutez les champignons sautés et le parmesan. Servez chaud."),
('Pasta Carbonara', '30', 2, 4, '2', 2, 6, 'pasta_carbonara.jpg', "Étape 1: Faites cuire les pâtes dans une grande casserole d\'eau bouillante salée jusqu\'à ce qu\'elles soient al dente. Étape 2: Pendant ce temps, faites revenir les lardons dans une poêle jusqu'à ce qu'ils soient croustillants. Étape 3: Dans un bol, mélangez les jaunes d\'œufs, le parmesan et le poivre. Étape 4: Égouttez les pâtes et réservez une louche d'eau de cuisson. Étape 5: Ajoutez les pâtes cuites à la poêle avec les lardons et mélangez bien. Étape 6: Retirez la poêle du feu et ajoutez le mélange d'œufs et de fromage. Remuez rapidement pour enrober les pâtes. Ajoutez un peu d'eau de cuisson si nécessaire pour obtenir une consistance crémeuse. Servez chaud."),
('Tiramisu', '60', 3, 4, '8', 2, 7, 'tiramisu.jpg', "Étape 1: Préparez le café fort et laissez-le refroidir. Étape 2: Séparez les blancs des jaunes d'œufs. Fouettez les jaunes avec le sucre jusqu'à ce que le mélange blanchisse. Ajoutez le mascarpone et mélangez jusqu'à obtenir une crème lisse. Étape 3: Battez les blancs d'œufs en neige ferme. Incorporez-les délicatement à la crème au mascarpone. Étape 4: Trempez rapidement les biscuits dans le café refroidi et disposez-les dans un plat. Étape 5: Versez la moitié de la crème mascarpone sur les biscuits. Répétez avec une autre couche de biscuits et de crème. Étape 6: Saupoudrez de cacao en poudre sur le dessus. Réfrigérez pendant au moins 4 heures avant de servir."),
('Boeuf bourguignon', '120', 2, 5, '8', 3, 8, 'boeuf_bourguignon.jpg', "Étape 1: Faites revenir les morceaux de bœuf dans une cocotte avec de l'huile d'olive. Étape 2: Ajoutez les oignons, les carottes, l'ail, et faites cuire quelques minutes. Étape 3: Ajoutez le vin rouge et le bouillon de bœuf. Étape 4: Laissez mijoter à feu doux pendant environ 2 heures. Étape 5: Ajoutez les champignons et laissez mijoter encore 30 minutes. Étape 6: Servez chaud avec des pommes de terre ou des pâtes."),
('Coq au vin', '120', 2, 5, '4', 3, 9, 'coq_au_vin.jpg', "Étape 1: Faites dorer le coq dans une cocotte avec du beurre et de l'huile. Étape 2: Ajoutez les oignons, les carottes, et l'ail, et faites revenir quelques minutes. Étape 3: Ajoutez le vin rouge, le bouillon de poulet, et les herbes de Provence. Étape 4: Laissez mijoter à feu doux pendant environ 2 heures. Étape 5: Ajoutez les champignons et laissez mijoter encore 30 minutes. Étape 6: Servez chaud avec des pommes de terre ou du riz."),
('Ratatouille', '60', 9, 5, '4', 2, 10, 'ratatouille.jpg', "Étape 1: Faites chauffer de l'huile d'olive dans une grande poêle et ajoutez les oignons et l'ail. Étape 2: Ajoutez les poivrons, les courgettes, les aubergines, et les tomates. Étape 3: Laissez mijoter à feu doux pendant environ 45 minutes, en remuant de temps en temps. Étape 4: Assaisonnez avec du sel, du poivre, et des herbes de Provence. Étape 5: Servez chaud avec du pain frais."),
('Quiche Lorraine', '45', 2, 5, '4', 2, 11, 'quiche_lorraine.jpg', "Étape 1: Préchauffez votre four à 180°C. Étape 2: Étalez la pâte brisée dans un moule à tarte. Étape 3: Faites revenir les lardons dans une poêle jusqu'à ce qu'ils soient croustillants. Étape 4: Dans un bol, battez les œufs avec la crème fraîche et le fromage râpé. Étape 5: Ajoutez les lardons et mélangez bien. Étape 6: Versez le mélange sur la pâte et enfournez pendant 30 à 35 minutes, jusqu'à ce que la quiche soit dorée."),
("Soupe à l'oignon", '60', 1, 5, '4', 2, 12, 'soupe_oignon.jpg', "Étape 1: Faites fondre le beurre dans une grande casserole et ajoutez les oignons émincés. Étape 2: Laissez cuire à feu doux pendant environ 30 minutes, jusqu'à ce que les oignons soient dorés et caramélisés. Étape 3: Ajoutez la farine et remuez pendant quelques minutes. Étape 4: Versez le bouillon de bœuf et le vin blanc et portez à ébullition. Étape 5: Réduisez le feu et laissez mijoter pendant 20 à 30 minutes. Étape 6: Servez chaud avec des croûtons et du fromage râpé."),
('Sushi', '45', 2, 3, '4', 3, 13, 'sushi.jpg', "Étape 1: Cuire le riz à sushi selon les instructions sur l'emballage et laisser refroidir. Étape 2: Préparer le vinaigre de riz en mélangeant le vinaigre de riz, le sucre et le sel. Étape 3: Incorporer délicatement le vinaigre de riz dans le riz cuit pour faire le riz à sushi. Étape 4: Étaler une fine couche de riz sur une feuille d'algue nori. Étape 5: Ajouter une bande de poisson cru, de légumes ou d'œufs sur le riz. Étape 6: Rouler l'algue nori avec les ingrédients à l'intérieur et couper en morceaux. Servez avec de la sauce soja et du wasabi."),
('Ramen', '60', 2, 3, '2', 2, 14, 'ramen.jpg', "Étape 1: Faites cuire les œufs à la coque et réservez. Étape 2: Dans une casserole, faites chauffer le bouillon de poulet avec la sauce soja, le mirin, et le gingembre râpé. Étape 3: Ajoutez les nouilles ramen et laissez cuire selon les instructions sur l'emballage. Étape 4: Pendant ce temps, faites sauter les légumes dans une poêle avec de l'huile de sésame. Étape 5: Une fois les nouilles cuites, versez-les dans un bol. Étape 6: Ajoutez le bouillon chaud, les légumes sautés et les œufs coupés en deux sur le dessus. Servez chaud."),
('Poulet aux amandes revisité', '45', 2, 6, '3', 2, 15, 'poulet_amandes_revisite.jpg', "Étape 1: Mariner le poulet coupé en dés dans une sauce à base de sauce soja, de miel et de gingembre râpé pendant 30 minutes. Étape 2: Pendant ce temps, faire sauter les amandes dans une poêle jusqu\'à ce qu\'elles soient dorées, puis les retirer de la poêle et les réserver. Étape 3: Dans la même poêle, faire sauter le poulet mariné jusqu\'à ce qu\'il soit doré et bien cuit. Étape 4: Ajouter les légumes de votre choix (poivrons, brocolis, carottes, etc.) dans la poêle avec le poulet et faire sauter pendant quelques minutes. Étape 5: Incorporer les amandes sautées réservées dans la poêle et mélanger. Étape 6: Servir chaud avec du riz cuit à la vapeur."),
('Burger américain', '30', 2, 2, '4', 2, 16, 'burger.jpg', "Étape 1: Préparer les ingrédients pour le burger : pains à burger, steaks hachés, tranches de fromage, laitue, tomate, oignon, etc. Étape 2: Faire cuire les steaks hachés à la poêle ou sur le grill jusqu'à ce qu'ils soient bien cuits. Étape 3: Pendant ce temps, toaster les pains à burger et préparer les garnitures. Étape 4: Assembler les burgers en plaçant les steaks cuits sur les pains grillés et en ajoutant les garnitures de votre choix. Étape 5: Servir chaud avec des frites ou des chips."),
('Tacos mexicains', '30', 2, 1, '4', 2, 17, 'tacos.jpg', "Étape 1: Préparer les ingrédients pour les tacos : tortillas, viande hachée assaisonnée, salsa, guacamole, fromage râpé, etc. Étape 2: Faire chauffer les tortillas dans une poêle ou au micro-ondes. Étape 3: Pendant ce temps, faire cuire la viande hachée assaisonnée dans une poêle jusqu'à ce qu'elle soit bien cuite. Étape 4: Assembler les tacos en plaçant une portion de viande cuite sur chaque tortilla chauffée et en ajoutant les garnitures de votre choix. Étape 5: Servir chaud avec des quartiers de citron vert et de la sauce piquante."),
('Salade grecque', '15', 1, 10, '2', 1, 18, 'salade_grecque.jpg', "Étape 1: Préparer les ingrédients pour la salade : concombres, tomates, oignons rouges, olives kalamata, fromage feta, huile d'olive, vinaigre de vin rouge, origan, sel et poivre. Étape 2: Couper les concombres, les tomates et les oignons rouges en dés et les placer dans un grand bol. Étape 3: Ajouter les olives kalamata et le fromage feta émietté dans le bol. Étape 4: Assaisonner la salade avec de l'huile d'olive, du vinaigre de vin rouge, de l'origan, du sel et du poivre selon votre goût. Étape 5: Mélanger délicatement et servir frais."),
('Sangria espagnole', '15', 5, 12, '8', 1, 19, 'sangria.jpg', "Étape 1: Préparer les ingrédients pour la sangria : vin rouge, fruits frais (oranges, citrons, pommes, etc.), sucre, triple sec, brandy, eau pétillante. Étape 2: Couper les fruits frais en tranches ou en quartiers et les placer dans un grand pichet. Étape 3: Ajouter le vin rouge, le sucre, le triple sec et le brandy dans le pichet. Étape 4: Remuer doucement pour mélanger les ingrédients. Étape 5: Réfrigérer pendant au moins 2 heures pour permettre aux saveurs de se mélanger. Étape 6: Avant de servir, ajouter de l'eau pétillante pour donner de l'effervescence à la sangria. Étape 7: Servir frais dans des verres à vin avec des glaçons."),
('Paella espagnole', '60', 2, 12, '4', 3, 20, 'paella.jpg', "Étape 1: Préparer les ingrédients pour la paella : riz à paella, poulet, chorizo, fruits de mer (moules, crevettes, calamars), tomates, poivrons, petits pois, safran, bouillon de poulet. Étape 2: Faire chauffer de l'huile d'olive dans une grande poêle ou une paellera. Étape 3: Faire dorer le poulet et le chorizo dans l'huile chaude. Étape 4: Ajouter les tomates, les poivrons et les petits pois dans la poêle et faire revenir jusqu'à ce qu'ils soient tendres. Étape 5: Incorporer le riz à paella dans la poêle et mélanger avec les autres ingrédients. Étape 6: Disposer les fruits de mer sur le dessus du riz. Étape 7: Saupoudrer de safran et verser le bouillon de poulet chaud dans la poêle. Étape 8: Laisser mijoter à feu moyen jusqu'à ce que le riz soit cuit et que les fruits de mer soient bien cuits. Étape 9: Servir chaud avec des quartiers de citron vert."),
('Pad Thai', '30', 4, 2, '2', 2, 21, 'pad_thai.jpg', "Étape 1: Faites tremper les nouilles de riz dans l'eau chaude pendant environ 10 minutes, puis égouttez-les. Étape 2: Dans une poêle chaude, faites revenir l'ail et l'échalote dans de l'huile jusqu'à ce qu'ils soient dorés. Étape 3: Ajoutez les crevettes et faites-les cuire jusqu'à ce qu'elles soient roses. Étape 4: Poussez les crevettes sur un côté de la poêle et cassez un œuf dans l'autre côté. Battez l'œuf et faites-le cuire légèrement, puis mélangez-le avec les crevettes. Étape 5: Ajoutez les nouilles de riz trempées dans la poêle et mélangez bien avec les crevettes et l'œuf. Étape 6: Ajoutez la sauce Pad Thai et mélangez jusqu'à ce que tout soit bien enrobé. Étape 7: Ajoutez les germes de soja et les arachides hachées, puis mélangez à nouveau. Servez chaud.");

Select * FROM recettes;

delete from utilisateurs where id = 23;
UPDATE Recettes SET photo = '../static/photos/food.png';