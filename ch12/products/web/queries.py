from ariadne import QueryType
from web.data import ingredients, products
from itertools import islice
from excepions import ItemNotFoundError

query = QueryType()


def get_page(items, items_per_page, page):
    if items_per_page is None or items_per_page <= 0:
        items_per_page = 10
    if page is None or page < 1:
        page = 1
    page = page - 1
    start = items_per_page * page if page > 0 else 0
    stop = start + items_per_page
    return list(islice(items, start, stop))


@query.field('allIngredients')
def resolve_all_ingredients(*_):
    return ingredients


@query.field('allProducts')
def resolve_all_products(*_):
    return products


@query.field('products')
def resolve_products(*_, input=None):
    filtered = [product for product in products]
    if input is None:
        return filtered

    if input.get('available') is not None:
        filtered = [
            product for product in filtered
            if product['available'] is input['available']
        ]

    if input.get('minPrice') is not None and input['minPrice'] is not None:
        filtered = [
            product for product in filtered
            if product.get('price') and product['price'] >= input['minPrice']
        ]
    if input.get('maxPrice') is not None and input['maxPrice'] is not None:
        filtered = [
            product for product in filtered
            if product.get('price') and product['price'] <= input['maxPrice']
        ]

    if input.get('sort') is not None and input.get('sortBy') is not None:
        try:
            filtered.sort(
                key=lambda product: (product.get(input['sortBy']) or '', type(
                    product.get(input['sortBy'])).__name__),
                reverse=input['sort'] == 'DESCENDING'
            )
        except (TypeError, KeyError):
            # If sorting fails, return unsorted
            pass

    page = input.get('page', 1)
    results_per_page = input.get('resultsPerPage', 10)
    return get_page(filtered, results_per_page, page)


@query.field('product')
def resolve_product(*_, id):
    if not id:
        raise ItemNotFoundError(f'Product with ID {id} not found')
    for product in products:
        if str(product['id']) == str(id):
            return product
    raise ItemNotFoundError(f'Product with ID {id} not found')


@query.field('ingredient')
def resolve_ingredient(*_, id):
    if not id:
        raise ItemNotFoundError(f'Ingredient with ID {id} not found')
    for ingredient in ingredients:
        if str(ingredient['id']) == str(id):
            return ingredient
    raise ItemNotFoundError(f'Ingredient with ID {id} not found')
