from .models import ShoppingList, Tag


def purchases_processor(request):
    if request.user.is_authenticated:
        purchases_count = ShoppingList.objects.filter(
            user=request.user).count()
    else:
        purchases_count = len(request.session.get('shopping_list', []))

    return {'purchases_count': purchases_count}


def url_parse(request):
    """Установка фильтров в урл страницы."""

    result_str = ''
    for item in request.GET.getlist('filters'):
        result_str += f'&filters={item}'
    return {'filters': result_str}


def all_tags(request):
    return {'all_tags': Tag.objects.all()}
