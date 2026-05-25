from models.product_model import Product
from sqlalchemy.orm import Session

from schemas.product_schema import ProductRequest


def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(product_id: int,db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        return product
    return {"message": "Product not found"}


def add_product(product_request: ProductRequest, db: Session):
    db.add(Product(**product_request.model_dump()))
    db.commit()

def update_product(product_id: int, product_request: ProductRequest,db: Session ):
    product = db.query(Product).filter(Product.id == product_id).first()
    print("product {}".format(product))
    if product:
        product.description = product_request.description
        db.commit()
        return product
    else:
        return {"message": "Product not found"}

def delete_product(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return {"message": "Product deleted"}
    else:
        return {"message": "Product not found"}




