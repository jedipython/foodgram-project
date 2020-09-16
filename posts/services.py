def get_ingredients(request):
    ingredients = []
    for key in request.POST:
        if key.startswith('nameingredient'):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST[
                'valueingredient_' + value_ingredient
            ]
    return ingredients
    