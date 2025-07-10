## ML-Powered Text Moderation API(Toxicity Filter as a Service)
This project is an API servicee for detecting toxic content and spam, powered by two machine learning models and built with Django. It includes an API key authentication system with usage limtis to control access.

# Features
- Toxic Text Detection  
  Detects:
    - dentity hate
    - Insult
    - Obsence
    - Threat
-Spam classification
  Classifies text as Spam or Ham
- API Key System
  -   Each user get a unique API Key
  -   API Usage is limited per Key
  -   Keys

  ## Tech Stack
  ML Models:
    - Scikit learn
  Backend:
    - Django
    - Django RESTFramework
    - Postgresql as database
 

```
text_moderation/
├── api
│ ├── models.py 
│ ├── views.py 
│ ├── urls.py 
│ ├── serializers.py
│ ├── permissions.py             # Custom API key permission logic
│ ├── tasks.py                       # background tasks
│ └── ...
├── train_model/                   # Machine learning models and notebooks
│ ├── toxic_model.pkl 
│ ├── spam_model.pkl 
│ └── model_training.ipynb
│
├── text_moderation/           # Main Django project configuration
│ ├── settings.py 
│ ├── urls.py 
│ └── ...
├── manage.py 
├── requirements.txt # Python dependencies
└── README.md 

```

## Installation
1. Clone the repository

  
2. Install a virtual environment:
```sh
pip install virtualenv
```
3. Create a virtual environment and activate it:
```sh
py -m venv myenv

myenv/scripts/activate
 ```
`myenv` is the name of the environment folder.

Install dependencies:
```sh
py -m pip install -r requirements.txt
```
Make initial migrations:
```bash
python manage.py makemigrations

python manage.py migrate
```
Start the backend development server:
```bash
python manage.py runserver
```



