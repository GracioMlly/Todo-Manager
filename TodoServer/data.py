from classes.Task import Task
from classes.Category import Category
from queue import PriorityQueue, LifoQueue

# Liste des tâches
tasksList: list[Task] = []

# La file des tâches par date de priorité
tasksByDeadline = PriorityQueue()

# La pile des tâches par ordre de priorité
tasksByPriorityOrder = LifoQueue()

# La liste des catégories
sans_categorie = Category(name="Sans catégorie")
categoriesList: list[Category] = [sans_categorie]

# La liste des sous-catégories
subcategoriesList: list[Category] = []