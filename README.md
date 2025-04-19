# Algorithme du plus cour chemin Dijkstra A*
 Ce repositiory permet de visualiser le fonctionnement des algorithmes de Dijkstra et A*
## Les fichiers
 Il est composé de deux fichiers indispensables pour son fonctionnement.
 
 Le premier fichier ***PathFinding.py***, qui contient l'ensemble du code permettant la recherche du plus court chemin.

 Le second fichier ***Visualisation_Infinite_Grid.py***, qui permet de constuire la grille ou la carte que le fichier ***PathFinding.py*** traitera, de visualiser le plus court chemin entre deux points. Tout cela peut-être fait sur une grille infinie.
### PathFinding.py
 Le fichier est composé d'une class *PathFinding*, qui prend plusieurs paramètres en entré.
 | Nom du paramètre | Type du paramètre | Description |
 | --- | --- | --- |
 | `_size` | `tuple -> taille 2 -> (x,y)` | Correpond au dimension de la liste traité par l'algorithme. |
 | `_start_point` | `tuple -> taille 2 -> (x,y)` | Correspond au coordonnée du point de départ dans la liste traité par l'algorithme. |
 | `_end_point` | `tuple -> taille 2 -> (x,y)` | Correspond au coordonnée du point d'arrivé dans la liste traité par l'algorithme. |
 | `_grid` | `list -> taille _size[0]*_size[1]` | Correspond aux coorodonnées de la grille en haut à gauche puis en bàs à droite de la grille donné à l'algorithme du plus court chemin. |

 Pour influencer la manière avec laquelle l'algorithme cherche, il faut modifier certaines informations présententes dans la fonction *Get_Node_Connected_To_Current*.

 La ligne utilisant la fonction *append* sur la liste *lst_inter*, possède deux coefficients essentiels. Dans le cas où le premier coefficient est de 0,5 et le second strictement positif, l'algorithme se comporte comme A*. Dans le cas où le premier coefficient est de 1 et le second nul, l'algorithme se comporte comme Dijkstra. Libre à vous de modifier ces coefficients tels que vous le souhaitez pour découvrir des actions très étonantes.

 Les délimitations de la grille donné à l'algorithme du plus court chemin, sont représentées par des cases turquoises
 
### Visualisation_Infinite_Grid.py
 Le fichier est composé d'une class *Window*, qui prend plusieurs paramètres en entré.
 | Nom du paramètre | Type du paramètre | Description |
 | --- | --- | --- |
 | `_screen_size` | `tuple -> taille 2 -> (x,y)` | Correpond au dimension de la fenêtre. |
 | `_grid_size` | `tuple -> taille 2 -> (x,y)` | Correpond au dimension de la liste d'affichage des cases. |
 | `_dim_tile` | `int` | Dimension d'une case en pixel. |
 | `_map_pathfinding_coor` | `tuple -> taille 2 -> ((x,y), (x,y))` | Correpond au dimension de la fenêtre. |

 Pour lancer la recherche d'un plus court chemin, il faut appuyer sur la touche *S*, sur un clavier AZERTY.

 Pour modifier le nombre d'image par seconde, il faut appuyer sur la touche *A* sur un clavier AZERTY.
 
 Pour effacer les cases de l'algorithme du plus court chemin, il faut appuyer sur la touche *C* sur un clavier AZERTY.
 
 Pour créer des murs, il suffi d'appuyer sur le *clique gauche* de la souris. La case choisi devient alors blanche.

 Pour initialiser le case de départ, il faut appuyer sur le *clique molette*  de la souris. La case choisi devient alors verte.

 Pour initialiser le case d'arrivé, il faut appuyer sur le *clique droit* de de la souris. La case choisi devient alors bleue.

 
