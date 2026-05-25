from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Request
from core.database import get_db
from core.limiter import limiter
from schemas.product_schema import ProductRequest
from services import product_service
from models.product_model import Product


product_router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@product_router.get("/")
@limiter.limit("5/minute")
def get_all_products(
        request: Request,
        db: Session = Depends(get_db)
):
    return product_service.get_all_products(db)

#--------------------------------------------------

@product_router.get("/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product= db.query(Product).filter(Product.id == id).first()
    if product:
        return product
    else:
        HTTPException(status_code=404, detail="Product not found")
    return None
#----------------------------------------------------------

@product_router.post("/")
def add_product(product: ProductRequest, db: Session = Depends(get_db)):
    try:
        return product_service.add_product(db, product)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
#--------------------------------------------------------------

@product_router.put("/{id}")
def update_product(id: int, updated_product: ProductRequest, db: Session = Depends(get_db)):
    print("update_product")
    product = db.query(Product).filter(Product.id == id).first()
    print("product {}".format(product))
    if product:
        product.description = updated_product.description
        db.commit()
        return product
    else:
        return {"message": "Product not found"}

#-------------------------------------------------

@product_router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if product:
        db.delete(product)
        db.commit()
        return {"message": "Product deleted"}
    else:
        return {"message": "Product not found"}



