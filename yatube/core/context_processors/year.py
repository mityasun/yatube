import datetime


def year(request):
    """Добавляет в контекст переменную greeting с приветствием."""
    now = datetime.datetime.now()
    return {
        'year': now.year,
    }
