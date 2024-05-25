# Install dependencies from requirements.txt
pip install django

pip install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic
