from pydantic import BaseModel
from classes.Task import Task
from typing import ClassVar
from uuid import uuid4


class Category(BaseModel):
    # Classe utilisée pour la création d'une catégorie

    id: str | None = None  # Son id
    name: str  # Son nom
    tasks: list[Task] | None = None  # Sa liste de tâche
    subcategories: list["Category"] | None = None  # Sa liste de sous-catégories

    all_categories_name: ClassVar[list[str]] = [
        "Sans catégorie"
    ]  # Liste des noms de toutes les catégories crées ~ Variable statique

    # Utilisation d'un keyword argument ~ args
    def __init__(self, **args):

        # Déballage de args
        super().__init__(**args)

        # Initialisation de la liste des tâches vides et l'id
        if self.tasks == None:
            self.tasks = []
        if self.id == None:
            self.id = str(uuid4())
        self.subcategories = []

    # Ajoute une tâche dans la liste des tâches de la catégorie
    def add_task(self, task: Task):
        self.tasks.append(task)

    # Supprime une tâche de la liste des taches de la catégorie
    def delete_task(self, value: Task | str):
        try:
            # Traitement de suppression suivant la valeur de 'value'
            if type(value) is str:
                task = next(task for task in self.tasks if task.id == value)
                self.tasks.remove(task)
            else:
                self.tasks.remove(value)
        except Exception as error:
            print(error)

    # Ajoute une sous-catégorie dans la liste des sous-catégories de la catégorie
    def add_subcategory(self, subcategory: "Category"):
        self.subcategories.append(subcategory)

    # Supprime une sous-catégorie dans la liste des sous-catégories de la catégorie
    def delete_subcategory(self, value: str):
        try:
            # Traitement de suppression suivant le type de 'value'
            if type(value) is str:
                subcategory = next(
                    subcategory
                    for subcategory in self.subcategories
                    if subcategory.id == value
                )
                self.subcategories.remove(subcategory)
            else:
                self.subcategories.remove(value)
        except Exception as error:
            print(error)
