@echo off

:: Créez et activez un environnement virtuel Python
python -m venv env
call env\Scripts\activate

:: Installez les dépendances
pip install -r .\backend\requirements.txt

:: Installez les packages frontend
cd frontend\bar-app
npm install
cd ..\..

:: Lancer Uvicorn dans un nouveau terminal
start cmd /k "cd backend && .\env\Scripts\activate && uvicorn app.main:app --reload"

:: Lancer npm dans un nouveau terminal
start cmd /k "cd frontend\bar-app && .\env\Scripts\activate && npm run start"
