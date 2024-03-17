from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from classes.Task import Task
from classes.Category import Category
from queue import PriorityQueue, LifoQueue
from uuid import uuid4

from data import (
    tasksList,
    tasksByDeadline,
    tasksByPriorityOrder,
    categoriesList,
    subcategoriesList,
)

app = FastAPI()

origins = ["http://localhost:5173"]  #

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###############################################################################################
""" Gestion des tâches """


# Pour récupérer la liste des tâches
@app.get("/tasks")
async def get_tasks(filter: str | None = None):
    # 'filter' est un paramètre de requête de l'url /tasks?filter=
    try:
        if filter == "date":
            return sorted(tasksByDeadline.queue, key=lambda task: task.deadline)
        elif filter == "order":
            return sorted(
                tasksByPriorityOrder.queue, key=lambda task: task.priority, reverse=True
            )
        else:
            return tasksList
    except Exception as error:
        print(error)
        return {"message": f"Le filtrage n'a pas pu avoir lieu"}


# Pour créer une tâche
@app.post("/tasks")
async def create_task(task: Task):
    # On reçoit de la requête les infos de création dans le paramètre 'task'
    try:
        # On initialise une tâche
        # Model_dump retourne() un dictionnaire
        # **task.model_dump() déballe le dictionnaire sous forme de clé - valeurs
        newTask = Task(**task.model_dump())

        tasksList.append(newTask)  # On ajoute la tâche dans la liste des tâches

        tasksByDeadline.put_nowait(newTask)  # On ajoute la tache dans la file
        tasksByPriorityOrder.put_nowait(newTask)  # On ajoute la tache dans la pile

        category_manager(newTask, categoriesList)  # Gestion de la catégorie
        return {"message": "La tâche a été ajoutée", "tâche": newTask}
    except Exception as error:
        print(error)
        return {"message": "La tâche n'a pas été crée"}


# Pour modifier une tâche
@app.put("/tasks/{taskId}")
async def update_task(taskId: str, task: Task):
    # On récupère dans le paramètre 'taskId' l'id de la tâche avec l'url /tasks/{taskId}
    # On reçoit de la requête les infos de modification dans le paramètre 'task'
    try:
        # On cherche la tâche à modifier
        taskToUpdate = next(task for task in tasksList if task.id == taskId)

        # Si la catégorie de la tâche à modifier change
        # On met à jour les catégories correspondantes
        if taskToUpdate.category != task.category:
            update_task_category(taskToUpdate, task)

        # Si la sous-catégorie de la tâche à modifier change
        # On met à jour les sous-catégories correspondantes
        if taskToUpdate.subcategory != task.subcategory:
            # rootCategory = next(
            #     category
            #     for category in categoriesList
            #     if category.name == taskToUpdate.category
            # )
            update_task_category(
                taskToUpdate, task, isRoot=False
            )

        # On met à jour finalement la tâche
        taskToUpdate.update(**task.model_dump())
        return {"message": "La tâche a été mise à jour", "tâche": taskToUpdate}
    except Exception as error:
        print(error)
        return {"message": "La tâche n'a pas été mise à jour"}


# Pour supprimer une tâche
@app.delete("/tasks/{taskId}")
async def delete_task(taskId: str):
    # On récupère dans le paramètre 'taskId' l'id de la tâche avec l'url /tasks/{taskId}
    global tasksList  # -> pour accéder à la liste de toutes les tâches
    try:
        # On cherche la tache à supprimer
        # On la retire de la liste des tâches
        taskToDelete = next(task for task in tasksList if task.id == taskId)
        tasksList.remove(taskToDelete)

        # On met à jour la file, pile et la catégorie correspondante
        priority_lists_updater(tasksByDeadline)
        priority_lists_updater(tasksByPriorityOrder)
        category_tasks_updater(taskToDelete, categoriesList)
        return {"message": "La tâche a été supprimée", "tâche": taskToDelete}
    except Exception as error:
        print(error)
        return {"message": f"La tâche avec l'Id {taskId} n'existe pas"}


###############################################################################################
""" Gestion des catégories """


# Pour récupérer la liste de catégories
@app.get("/categories")
async def get_categories():
    return categoriesList


# Pour créer une catégorie
@app.post("/categories")
async def create_category(category: Category):
    # On récupère les infos de création dans le paramètre 'category'
    try:
        # On initialise une catégorie
        # Model_dump() retourne un dictionnaire
        # **category.model_dump() déballe le dictionnaire sous forme de clé - valeurs
        newCategory = Category(**category.model_dump())

        # On vérifie si la catégorie initialisée existe déjà
        isPresent = does_this_category_already_exist(newCategory.name, categoriesList)

        if isPresent:
            return {"message": f"La catégorie {newCategory.name} existe déjà"}
        else:
            # Si elle n'existe pas déjà, on ajoute son son nom dans la liste de nom des catégories
            # On l'ajoute dans la liste des catégories
            Category.all_categories_name.append(category.name)
            categoriesList.append(newCategory)
            return {"message": "La catégorie a été ajoutée", "catégorie": newCategory}
    except Exception as error:
        print(error)
        return {"message": "La catégorie n'a pas été crée"}


# Pour supprimer une catégorie
@app.delete("/categories/{categoryId}")
async def delete_category(categoryId: str):
    # On récupère dans le paramètre 'categoryId' l'id de la category avec l'url /category/{categoryId}
    try:
        # On cherche la catégorie à supprimer
        categoryToDelete = next(
            category for category in categoriesList if category.id == categoryId
        )

        # On supprime les tâches de cette catégorie dans :
        # -> la liste des tâches
        # -> la file, la pile
        for task in categoryToDelete.tasks:
            tasksList.remove(task)
        priority_lists_updater(tasksByDeadline)
        priority_lists_updater(tasksByPriorityOrder)

        # On retire la catégorie dans la liste des catégories
        # On retire son nom dans la liste des noms des catégories
        categoriesList.remove(categoryToDelete)
        Category.all_categories_name.remove(categoryToDelete.name)

        return {
            "message": "La catégorie a été supprimée",
            "catégorie": categoryToDelete,
        }
    except Exception as error:
        print(error)
        return {"message": "La catégorie n'a pas pu être supprimée"}


# Pour créer une sous-catégorie
@app.post("/categories/{categoryId}")
async def create_subcategory(categoryId: str, subcategory: Category):
    # On récupère dans le paramètre 'categoryId' l'id de la category avec l'url /categories/{categoryId}
    # On reçoit de la requête les infos de création dans le paramètre 'subcategory'
    try:
        # On initialise une sous-catégorie
        newSubcategory = Category(**subcategory.model_dump())

        # On vérifie si la sous-catégorie initialisée existe déjà
        # Comme sous-catégorie dans la catégorie mère
        # Catégorie mère : 'rootCategory'
        rootCategory = next(
            category for category in categoriesList if category.id == categoryId
        )
        isPresent = does_this_category_already_exist(
            newSubcategory.name, rootCategory.subcategories
        )

        if isPresent:
            return {"message": f"La sous-catégorie {newSubcategory.name} existe déjà"}
        else:
            # Si elle n'existe pas on l'ajoute comme sous-catégorie
            # De rootCategory
            rootCategory.add_subcategory(newSubcategory)
            subcategoriesList.append(newSubcategory)
            return {
                "message": "La sous-catégorie a été crée",
                "sous-catégorie": newSubcategory,
            }
    except Exception as error:
        print(error)
        return {"message": "La sous-catégorie n'a pas été crée"}


###############################################################################################

""" Fonctions utilitaires """


# Met à jour la pile ou la file
def priority_lists_updater(structure: PriorityQueue | LifoQueue):
    # Le paramètre 'structure' est soit une file soit une pile
    # On copie la liste des tâches dans 'structure'
    structure.queue = tasksList.copy()


# Met à jour la liste des tâches d'une catégorie
def category_tasks_updater(task: Task, categoriesList: list[Category]):
    # Le paramètre 'task' est la tâche à supprimer
    # Le paramètre 'categoriesList' est la liste des catégories
    try:
        # On cherche la catégorie à mettre à jour
        categoryToUpdate = next(
            category for category in categoriesList if category.name == task.category
        )
        # On supprime la tâche de sa liste de tâches
        categoryToUpdate.delete_task(task)
    except Exception as error:
        print(error)


# Gère une catégorie et sa tâche
def category_manager(task: Task, categoriesList: list[Category]):
    # Le paramètre 'task' est la tâche
    # Le paramètre 'categoriesList' est la liste des catégories
    try:
        # Si la catégorie de la tâche existe
        if task.category in Category.all_categories_name:

            # On cherche la catégorie
            category = next(
                category
                for category in categoriesList
                if category.name == task.category
            )

            if task.subcategory == "":
                # On ajoute la tâche à sa liste de tâches
                category.add_task(task)
            else:
                subcategory = next(
                    subcategory
                    for subcategory in category.subcategories
                    if subcategory.name == task.subcategory
                )
                subcategory.add_task(task)
        else:

            # Si la catégorie n'existe pas on ajoute son nom dans la liste de nom des catégories
            # On crée une catégorie avec ce nom
            # On ajoute la tâche à sa liste de tâches
            # On ajoute la catégorie à liste de catégories
            Category.all_categories_name.append(task.category)
            category = Category(id=str(uuid4()), name=task.category)
            category.add_task(task)
            categoriesList.append(category)
    except Exception as error:
        print(error)
        return {"message": "Complications dans la gestion des catégories"}


# Vérifie si une catégorie existe déjà
def does_this_category_already_exist(name: str, categoriesList: list[Category]):
    # Le paramètre 'name' est le nom de la catégorie
    # Le paramètre 'categoriesList' est une liste de catégories
    try:
        # On recherche la catégorie
        category = next(
            category for category in categoriesList if category.name == name
        )
        if category:
            # Si elle existe on renvoie True
            return True
    except Exception as error:
        print("Catégorie non trouvée", error)
        # Sinon False
        return False


# Gère la mise à jour de catégorie d'une tâche
# def update_task_category(
#     taskToUpdate: Task, task: Task, categoriesList: list[Category], isRoot=True
# ):
#     # Le paramètre 'taskToUpdate' est la tâche dont la catégorie change
#     # Le paramètre 'task' est la tâche qui est censée remplacée 'taskToUpdate'
#     # Le paramètre 'categoriesList' est une liste de catégories
#     # Le paramètre 'isRoot' permet de séparer certains traitements des racines des noeuds
#     try:
#         # On récupère l'id de taskToUpdate
#         taskId = taskToUpdate.id

#         # On cherche l'ancienne catégorie
#         oldCategory = None

#         if isRoot:
#             oldCategory = next(
#                 category
#                 for category in categoriesList
#                 if category.name == taskToUpdate.category
#             )
#         else:
#             oldCategory = next(
#                 category
#                 for category in categoriesList
#                 if category.name == taskToUpdate.subcategory
#             )

#         # On vérifie si la nouvelle catégorie existe
#         if does_this_category_already_exist(task.category, categoriesList):
#             # On la recherche
#             newCategory = None

#             if isRoot:
#                 newCategory = next(
#                 category
#                 for category in categoriesList
#                 if category.name == task.category
#             )
#             else:
#                 newCategory = next(
#                 category
#                 for category in categoriesList
#                 if category.name == task.subcategory
#             )
#             # On lui ajoute la tâche à mettre à jour
#             newCategory.add_task(taskToUpdate)
#         else:
#             # Sinon on crée la nouvelle catégorie et on lui ajoute la tâche
#             print("pas trouvé")
#             category_manager(task, categoriesList)

#         # On supprime 'taskToUpdate' de l'ancienne catégorie
#         oldCategory.delete_task(taskId)

#         # Si la catégorie est une racine
#         if isRoot:
#             oldSubCategory = next(
#                 category
#                 for category in oldCategory.subcategories
#                 if category.name == taskToUpdate.subcategory
#             )
#             oldSubCategory.delete_task(taskId)

#     except Exception as error:
#         print(error)


def update_task_category(
    taskToUpdate: Task,
    task: Task,
    # categoriesList: list[Category],
    isRoot=True,
    allCategories: list[Category]=categoriesList,
    allSubcategories: list[Category]=subcategoriesList,
):
    # Le paramètre 'taskToUpdate' est la tâche dont la catégorie change
    # Le paramètre 'task' est la tâche qui est censée remplacée 'taskToUpdate'
    # Le paramètre 'categoriesList' est une liste de catégories
    # Le paramètre 'isRoot' permet de séparer certains traitements des racines des noeuds
    try:
        # On récupère l'id de taskToUpdate
        taskId = taskToUpdate.id

        # On cherche l'ancienne catégorie
        oldCategory = None
        newCategory = None

        # Traitement si c'est une racine
        if isRoot:
            oldCategory = next(
                category
                for category in allCategories
                if category.name == taskToUpdate.category
            )

            #  On vérifie si la nouvelle catégorie existe
            if does_this_category_already_exist(task.category, allCategories):
                # On la recherche
                newCategory = next(
                    category
                    for category in allCategories
                    if category.name == task.category
                )

                # On lui ajoute la tâche à mettre à jour
                newCategory.add_task(taskToUpdate)
            else:
                # Sinon on crée la nouvelle catégorie et on lui ajoute la tâche
                print("pas trouvé")
                category_manager(task, allCategories)

            #  On supprime 'taskToUpdate' de l'ancienne catégorie
            oldCategory.delete_task(taskId)

        else:
            # Traitement si c'est un simple noeud
            oldCategory = next(
                category
                for category in allSubcategories
                if category.name == taskToUpdate.subcategory
            )

            newCategory = next(
                category
                for category in allSubcategories
                if category.name == task.subcategory
            )

            newCategory.add_task(taskToUpdate)
            oldCategory.delete_task(taskId)

    except Exception as error:
        print(error)
