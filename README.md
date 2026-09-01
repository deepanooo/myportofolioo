# My Portfolio — Tutorial 0 & 1

## Setup (MacBook / macOS)

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## Important
- Do not upload `env/`
- Do not upload `.env`
- Keep the Django project folder name as `myportofolio`
