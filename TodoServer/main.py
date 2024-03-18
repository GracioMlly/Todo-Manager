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
# Complexité temporelle : O(nlogn)
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
# Complexité temporelle : O(n)
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

        # On ajoute la tâche dans la catégorie qu'il faut
        # (On ajoute la tâche dans la sous-catégorie qu'il faut)
        category_manager(newTask, categoriesList)
        return {"message": "La tâche a été ajoutée", "tâche": newTask}
    except Exception as error:
        print(error)
        return {"message": "La tâche n'a pas été crée"}


# Pour modifier une tâche
# Complexité temporelle : O(n)
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
            update_task_category(taskToUpdate, task, isRoot=False)

        # On met à jour finalement la tâche
        taskToUpdate.update(**task.model_dump())
        return {"message": "La tâche a été mise à jour", "tâche": taskToUpdate}
    except Exception as error:
        print(error)
        return {"message": "La tâche n'a pas été mise à jour"}


# Pour supprimer une tâche
# Complexité temporelle : O(n)
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
# Complexité temporelle : O(1)
@app.get("/categories")
async def get_categories():
    return categoriesList


# Pour créer une catégorie
# Complexité temporelle : O(n)
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
# Complexité temporelle : O(n)
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
# Complexité temporelle : O(n)
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


# Pour supprimer une sous-catégorie
# Complexité temporelle : O(n^2)
@app.delete("/categories/{categoryId}/{subcategoryId}")
async def delete_subcategory(categoryId: str, subcategoryId: str):
    # On récupère dans le paramètre 'categoryId' l'id de la category avec l'url /category/{subcategoryId}
    # On récupère dans le paramètre 'subcategoryId' l'id de la sous-catégorie avec l'url /category/{subcategoryId}
    try:
        # On cherche la sous-catégorie à supprimer
        rootCategory = next(
            category for category in categoriesList if category.id == categoryId
        )

        subcategoryToDelete = next(
            category
            for category in rootCategory.subcategories
            if category.id == subcategoryId
        )

        # On supprime les tâches de cette sous-catégorie dans :
        # -> la liste des tâches
        # -> la file, la pile
        # -> la catégorie (Racine)
        for task in subcategoryToDelete.tasks:
            tasksList.remove(task)
            category_tasks_updater(task, categoriesList)
        priority_lists_updater(tasksByDeadline)
        priority_lists_updater(tasksByPriorityOrder)

        # On retire la sous-catégorie de la catégorie Racine
        rootCategory.delete_subcategory(subcategoryToDelete)

        return {
            "message": "La sous-catégorie a été supprimée",
            "sous-catégorie": subcategoryToDelete,
        }
    except Exception as error:
        print(error)
        return {"message": "La sous-catégorie n'a pas pu être supprimée"}


###############################################################################################

""" Fonctions utilitaires """


# Met à jour la pile ou la file
# Complexité temporelle : O(n)
def priority_lists_updater(structure: PriorityQueue | LifoQueue):
    # Le paramètre 'structure' est soit une file soit une pile
    # On copie la liste des tâches dans 'structure'
    structure.queue = tasksList.copy()


# Pour la suppression des tâches d'une catégorie
# Complexité temporelle : O(n)
def category_tasks_updater(task: Task, categoriesList: list[Category]):
    # Le paramètre 'task' est la tâche à supprimer
    # Le paramètre 'categoriesList' est une liste des catégories
    try:
        # On cherche la catégorie à mettre à jour
        categoryToUpdate = next(
            category for category in categoriesList if category.name == task.category
        )
        # On supprime la tâche de sa liste de tâches
        categoryToUpdate.delete_task(task)

        if task.subcategory != "":
            subcategory = next(
                category
                for category in categoryToUpdate.subcategories
                if category.name == task.subcategory
            )
            subcategory.delete_task(task)
    except Exception as error:
        print(error)


# Assigne une tâche à sa catégorie correspondante
# Complexité temporelle : O(n)
def category_manager(task: Task, categoriesList: list[Category]):
    # Le paramètre 'task' est la tâche
    # Le paramètre 'categoriesList' est une liste de catégories
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
                category.add_task(task)
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
# Complexité temporelle : O(n)
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


# Gère les mises à jour de la catégorie / sous-catégorie d'une tâche
# Complexité temporelle : O(n)
def update_task_category(
    taskToUpdate: Task,
    task: Task,
    isRoot=True,
    allCategories: list[Category] = categoriesList,
):
    # Le paramètre 'taskToUpdate' est la tâche dont la catégorie change
    # Le paramètre 'task' est la tâche qui est censée remplacée 'taskToUpdate'
    # Le paramètre 'isRoot' permet de séparer certains traitements des racines des noeuds
    # Le paramètre 'allCategories' est la liste de catégories
    # Le paramètre 'allSubcategories' est la liste de sous-catégories
    try:
        # On récupère l'id de taskToUpdate
        taskId = taskToUpdate.id

        if isRoot:
            # Traitement si c'est un changement de catégorie
            # On cherche l'ancienne catégorie
            oldRootCategory = next(
                category
                for category in allCategories
                if category.name == taskToUpdate.category
            )

            # On cherche la nouvelle catégorie
            newRootCategory = next(
                category for category in allCategories if category.name == task.category
            )

            # Si la tâche à mettre à jour avait une sous-catégorie
            if taskToUpdate.subcategory != "":
                # On cherche la sous-catégorie
                oldSubcategory = next(
                    category
                    for category in oldRootCategory.subcategories
                    if category.name == taskToUpdate.subcategory
                )

                # On retire la tâche de la catégorie et de la sous-catégorie
                oldRootCategory.delete_task(taskId)
                oldSubcategory.delete_task(taskId)
            else:
                oldRootCategory.delete_task(taskId)

            # Si la tâche à mettre à jour possède une nouvelle sous-catégorie
            if task.subcategory != "":

                # On cherche la nouvelle sous-catégorie
                newSubCategory = next(
                    category
                    for category in newRootCategory.subcategories
                    if category.name == task.subcategory
                )

                # On ajoute la tâche à mettre à jour dans la nouvelle catégorie et sous-catégorie
                newRootCategory.add_task(taskToUpdate)
                newSubCategory.add_task(taskToUpdate)
            else:
                newRootCategory.add_task(taskToUpdate)

        else:
            # Traitement si c'est un changement de sous-catégorie

            # On cherche la catégorie
            rootCategory = next(
                category
                for category in allCategories
                if category.name == taskToUpdate.category
            )

            # Si la tâche à mettre à jour avait une sous-catégorie
            if taskToUpdate.subcategory != "":
                # On la cherche
                oldSubcategory = next(
                    category
                    for category in rootCategory.subcategories
                    if category.name == taskToUpdate.subcategory
                )
                # On retire cette tâche de la sous-catégorie
                oldSubcategory.delete_task(taskId)

            # Si la tâche à mettre à jour possède une nouvelle catégorie
            if task.subcategory != "":
                # On la cherche
                newSubCategory = next(
                    category
                    for category in rootCategory.subcategories
                    if category.name == task.subcategory
                )

                # On ajoute la tâche à mettre à jour dans la nouvelle sous-catégorie
                newSubCategory.add_task(taskToUpdate)

    except Exception as error:
        print(error)
