echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@mail.ru').exists() or User.objects.create_superuser('admin@mail.ru','admin','Administrations','Admin','Qwdfg145!')" | python manage.py shell