#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser if it doesn't already exist
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='tony').exists():
    User.objects.create_superuser(username='tony', email='tony@example.com', password='Frank@222')
    print('Superuser tony created.')
else:
    u = User.objects.get(username='tony')
    u.set_password('Frank@222')
    u.is_superuser = True
    u.is_staff = True
    u.is_active = True
    u.save()
    print('Superuser tony updated/verified.')
EOF

