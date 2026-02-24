
from ariadne import UnionType
from ariadne import ScalarType, InterfaceType, ObjectType
from datetime import datetime
import uuid
import copy

from web.data import ingredients, products, suppliers

product_type = UnionType('Product')
datetime_scalar = ScalarType('Datetime')
product_interface = InterfaceType("ProductInterface")
ingredient_type = ObjectType("Ingredient")
supplier_type = ObjectType("Supplier")


@product_type.type_resolver
def resolve_product_type(obj, *_):
    if 'hasFilling' in obj:
        return 'Cake'
    return 'Beverage'


@datetime_scalar.serializer
def serializer_datetime_scalar(date):
    return date.isoformat()


@datetime_scalar.value_parser
def parser_datetime_scalar(date):
    return datetime.fromisoformat(date)


@product_interface.field("ingredients")
def resolve_product_ingredients(product, _):
    recipe = [copy.copy(ingredient)
              for ingredient in product.get("ingredients", [])]
    for ingredient_recipe in recipe:
        ingredient_id = ingredient_recipe.get("ingredient")
        for ingredient in ingredients:
            if str(ingredient["id"]) == str(ingredient_id):
                ingredient_copy = copy.copy(ingredient)
                # Ensure lastUpdated exists
                if ingredient_copy.get("lastUpdated") is None:
                    ingredient_copy["lastUpdated"] = datetime.utcnow()
                ingredient_recipe["ingredient"] = ingredient_copy
                break
    return recipe


@ingredient_type.field("supplier")
def resolve_ingredient_suppliers(ingredient, _):
    if ingredient.get("supplier") is not None:
        for supplier in suppliers:
            if supplier["id"] == ingredient["supplier"]:
                return supplier


@supplier_type.field('ingredients')
def resolve_supplier_ingredient(supplier, _):
    return [
        ingredient
        for ingredient in ingredients
        if ingredient.get('supplier') == supplier['id']
    ]


@ingredient_type.field("products")
def resolve_ingredient_products(ingredient, _):
    result = []
    for product in products:
        for ingredient_recipe in product.get("ingredients", []):
            if str(ingredient_recipe.get("ingredient")) == str(ingredient["id"]):
                result.append(product)
                break
    return result
