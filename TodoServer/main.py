from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from classes.Task import Task
from classes.Category import Category
from queue import PriorityQueue, LifoQueue
from uuid import uuid4

from data import tasksList, tasksByDeadline, tasksByPriorityOrder, categoriesList

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
        return {"message": f"le filtrage n'a pas pu avoir lieu"}


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
        return {"message": "la tâche a été ajoutée", "tâche": newTask}
    except Exception as error:
        print(error)
        return {"message": "la tâche n'a pas été crée"}


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
            update_task_category(taskToUpdate, task, categoriesList)

        # On met à jour finalement la tâche
        taskToUpdate.update(**task.model_dump())
        return {"message": "la tâche a été mise à jour", "tâche": taskToUpdate}
    except Exception as error:
        print(error)
        return {"message": "la tâche n'a pas été mise à jour"}


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
        return {"message": "la tâche a été supprimée", "tâche": taskToDelete}
    except Exception as error:
        print(error)
        return {"message": f"la tâche avec l'Id {taskId} n'existe pas"}


###############################################################################################
""" Gestion des catégories """


# Pour récupérer la liste de catégories
@app.get("/categories")
async def get_categories():
    return categoriesList


# Pour créer une catégorie
@app.post("/categories")
async def create_task(category: Category):
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
            return {"message": "la catégorie a été ajoutée", "catégorie": newCategory}
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
            "message": "la catégorie a été supprimée",
            "catégorie": categoryToDelete,
        }
    except Exception as error:
        print(error)
        return {"message": "la catégorie n'a pas pu être supprimée"}


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

            # On ajoute la tâche à sa liste de tâches
            category.add_task(task)
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
    # Le paramètre 'categoriesList' est la liste des catégories
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
def update_task_category(
    taskToUpdate: Task, task: Task, categoriesList: list[Category]
):
    # Le paramètre 'taskToUpdate' est la tâche dont la catégorie change
    # Le paramètre 'task' est la tâche qui est censée remplacée 'taskToUpdate'
    # Le paramètre 'categoriesList' est la liste des catégories
    try:
        # On récupère l'id de taskToUpdate
        taskId = taskToUpdate.id

        # On cherche l'ancienne catégorie
        oldCategory = next(
            category
            for category in categoriesList
            if category.name == taskToUpdate.category
        )

        # On vérifie si la nouvelle catégorie existe
        if does_this_category_already_exist(task.category, categoriesList):
            # On la recherche
            newCategory = next(
                category
                for category in categoriesList
                if category.name == task.category
            )
            # On lui ajoute la tâche à mettre à jour
            newCategory.add_task(taskToUpdate)
        else:
            # Sinon on crée la nouvelle catégorie et on lui ajoute la tâche
            category_manager(task, categoriesList)

        # On supprime 'taskToUpdate' de l'ancienne catégorie
        oldCategory.delete_task(taskId)

    except Exception as error:
        print(error)
