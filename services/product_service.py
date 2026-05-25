from repositories import product_repository
from sqlalchemy.orm import Session

from schemas.product_schema import ProductRequest


def get_all_products(db: Session):
    products = product_repository.get_all_products(db)

    # business logic can go here
    # filtering
    # validations
    # transformations

    return products

def get_product_by_id(product_id: int, db: Session):
    product = product_repository.get_product_by_id(product_id,db)
    return product


def add_product(db: Session, product_request: ProductRequest ):
    product = product_repository.add_product(product_request, db)
    return product

def update_product(product_id: int, product_request: ProductRequest, db: Session):
    product = product_repository.update_product(product_id, product_request, db)
    return product

def delete_product(product_id: int, db: Session):
    product = product_repository.delete_product(product_id, db)
    return product

