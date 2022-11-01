import datetime


def year(request):
    """Добавляет в контекст переменную с актуальным годом."""
    now = datetime.datetime.now()
    return {
        'year': now.year,
    }
