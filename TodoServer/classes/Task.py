from pydantic import BaseModel
from datetime import date


class Task(BaseModel):
    # Classe utilisée pour la création d'une task / tâche / todo

    id: str  # Son id
    description: str  # Sa description
    priority: int  # Sa priorité
    deadline: date  # -> Sa deadline / date de fin
    category: str | None = None  # Sa catégorie

    # ** Nous permet de définir un keyword argument dans la définition d'une fonction
    # **args signifie donc que nous attendons un ensemble d'arguments sous forme de paires clé-valeurs
    # L'appel du constructeur attend donc les arguments sous cette forme :
    # Task(id = valeur, description = valeur, priority = valeur, deadline = valeur, category = valeur)
    def __init__(self, **args):

        # A l'intérieur d'une fonction un keyword argument est considéré comme un dictionnaire
        # Ici args équivaut à un dictionnaire
        # ** dans l'appelle d'une fonction permet de déballer un dictionnaire sous forme de paires clé-valeurs
        super().__init__(**args)

        # Si la tâche n'a pas de catégorie, elle a une valeur par défaut
        if self.category == None or self.category == "":
            self.category = "Sans catégorie"

    # Redéfinition de la méthode de comparaison < : Task1 < Task2
    def __lt__(self, other):
        # La comparaison de deux objets Task se fait par rapport à leur date
        return self.deadline.toordinal() < other.deadline.toordinal()

    # Mets à jour les attributs
    def update(
        self,
        id: str,
        description: str,
        priority: int,
        deadline: date,
        category: str | None = "",
    ):
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.category = category
