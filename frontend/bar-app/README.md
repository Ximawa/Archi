# Projet de archi N tier 


## Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre machine :
- Python 3.8+
- SQLlite
- Les dépendances Python listées dans `requirements.txt`

## Installation

1. Clonez ce dépôt :

    ```bash
    git clone https://github.com/Ximawa/Archi
    ```

2. Créez et activez un environnement virtuel Python :

    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
    ```

3. Installez les dépendances :

    ```bash
    pip install -r requirements.txt
    ```
4. Installez les packages :
   
   Dans le dossier frontend/bar-app/
        ```bash
       npm install 
       ```

## Utilisation

1. Lancez l'application avec Uvicorn :
    
    Dans le dossier backend
    ```bash
    uvicorn app.main:app --reload
    ```

2. Accédez à l'application :

    Dans le dossier frontend/bar-app/
    ```bash
    npm run start
    ```

