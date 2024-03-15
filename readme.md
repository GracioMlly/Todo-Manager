# Gestion de tâches


Une application web conçu pour la gestion de tâches (Lecture, Création, modification et suppression). Le front a été réalisé avec JavaScript (React.js) et le back avec Python (FastApi)

## Pour commencer

### Pré-requis

Ce qui est requis pour lancer le projet sur la machine

- Node.js
- Python


### Installation

Étapes à suivre pour installer les dépendances du projet.

1. Ouvrir le terminal puis installer FastApi

```bash
pip install "fastapi[all]"
```

2. Dans le terminal, se positionner dans le dossier **TodoApp** et installer les packages nodes

```bash
npm install
```

## Démarrage

Pour lancer le projet il faut mettre en marche le serveur du back et du front simultanément

1. Pour mettre en marche le back, dans le terminal se positionner dans le dossier **TodoServer** puis exécuter cette commande

```bash
uvicorn main:app --reload
```
2. Pour mettre en marche le front, dans un autre terminal se positionner dans le dossier **TodoApp** puis exécuter cette commande

```bash
npm run dev
```
Les liens des serveurs seront données dans le terminal.