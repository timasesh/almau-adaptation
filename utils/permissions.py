# utils/permissions.py
from django.http import HttpResponseForbidden


def position_required(*allowed_positions):
    """
    Декоратор для ограничения доступа по должности.
    Пример:
        @position_required('HR Manager', 'IT Support')
        def my_view(request):
            ...
    """

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("Требуется авторизация")

            user_position = getattr(getattr(user, "profile", None), "position", None)
            if not user_position or user_position.name not in allowed_positions:
                return HttpResponseForbidden("Нет доступа: ваша должность не позволяет войти")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
