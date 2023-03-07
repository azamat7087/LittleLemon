from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_queryset(**filter_data) -> User:
    return User.objects.filter(**filter_data)


def create_user(client_data):
    user_data = {
        key: value for key, value in client_data.items() if hasattr(User, key)
    }
    try:
        user = User.objects.get(email=user_data.get('email'))
    except User.DoesNotExist:
        user = User.objects.create(**user_data)
        user.set_password(User.objects.make_random_password())
        user.save()
    return user
