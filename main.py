from fastapi import FastAPI

from models import Product

app = FastAPI()

products = [
    Product(id=1, name="Phone", description="Phone", price=99, quantity=10 ),
    Product(id=2, name="laptop", description="laptop", price=999, quantity=6 )
]


@app.get("/")
def greeting():
    print("Welcome to home page")
    return {"message": "Welcome to home page"}
#--------------------------------------------

@app.get("/products")
def greeting():
    return products
#--------------------------------------------------

@app.get("/products/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
        else:
            return {"message": "Product not found"}
    return None
#----------------------------------------------------------

@app.post("/products")
def add_product(product: Product):
    products.append(product)
    return products
#--------------------------------------------------------------

@app.put("/products/{id}")
def update_product(id: int, updated_product: Product):
    for product in products:
        if product.id == id:
            product.name = updated_product.name
            product.description = updated_product.description
            product.price = updated_product.price
            product.quantity = updated_product.quantity
            return product


    return {"message": "Product not found"}
#-------------------------------------------------

@app.delete("/products/{id}")
def delete_product(id: int):
    for product in products:
        if product.id == id:
            products.remove(product)
            return products

    return {"message": "Product not found"}
