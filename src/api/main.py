from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from src.database.connection import (
    connect_to_db,
    get_all_products,
    get_product_by_id,
    create_order,
    get_all_users,
    get_user_by_id,
    create_user,
    update_product,
    delete_product
)



class OrderCreate(BaseModel):
    user_id: int
    products: list[tuple[int, int]]



class UserCreate(BaseModel):
    name: str
    email: str


class ProductUpdate(BaseModel):
    name: str
    price: int


app = FastAPI()


@app.get("/products", status_code=200)
def get_products(limit: int = 10, offset: int = 0):
    try:
        conn = connect_to_db()
        products = get_all_products(conn, limit, offset)
        conn.close()
        total = len(products)

        result = {
            "total": total,
            "limit": limit,
            "offset": offset,
            "products": products
        }
        return result
    except:
        raise HTTPException(status_code=500, detail="Ошибка на стороне сервера.")


@app.get("/products/{product_id}", status_code=200)
def get_product(product_id: int):
    try:
        conn = connect_to_db()
        product = get_product_by_id(conn, product_id)
        conn.close()
        return product.__dict__
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)
    except:
        raise HTTPException(status_code=500, detail="Ошибка на стороне сервера.")


@app.put("/products/{product_id}", status_code=200)
def product_update(product_id: int, product: ProductUpdate):
    try:
        conn = connect_to_db()
        get_product_by_id(conn, product_id)
        product = update_product(conn, product_id, product.name, product.price)
        conn.close()
        return product.__dict__
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)
    except:
        raise HTTPException(status_code=500, detail="Ошибка на стороне сервера.")


@app.delete("/products/{product_id}", status_code=200)
def product_delete(product_id: int):
    try:
        conn = connect_to_db()
        get_product_by_id(conn, product_id)
        delete_product(conn, product_id)
        conn.close()
        return {"message": f"Товар с id={product_id} удален."}
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)
    except:
        raise HTTPException(status_code=500, detail=f"Ошибка на стороне сервера.")


@app.post("/orders", status_code=201)
def order_create(order: OrderCreate):
    try:
        conn = connect_to_db()
        order = create_order(conn, order.user_id, order.products)
        conn.close()
        return order
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)
    except:
        raise HTTPException(status_code=500, detail=f"Ошибка на стороне сервера.")


@app.get("/users", status_code=200)
def get_users(limit: int=10, offset: int=0):
    try:
        conn = connect_to_db()
        users = get_all_users(conn, limit, offset)
        total = len(users)
        conn.close()

        result = {
            "total": total,
            "limit": limit,
            "offset": offset,
            "users": users
        }
        return result
    except:
        raise HTTPException(status_code=500, detail="Ошибка на стороне сервера.")


@app.get("/users/{user_id}", status_code=200)
def get_user(user_id: int):
    try:
        conn = connect_to_db()
        user = get_user_by_id(conn, user_id)
        conn.close()
        return user.__dict__
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)
    except:
        raise HTTPException(status_code=500, detail="Ошибка на стороне сервера.")


@app.post("/users", status_code=201)
def user_create(user: UserCreate):
    try:
        conn = connect_to_db()
        user_id = create_user(conn, user.name, user.email)
        conn.close()
        return {"id": user_id, "name": user.name, "email": user.email}
    except:
        raise HTTPException(status_code=500, detail="Ошибка на стороне сервера.")


def test_api():
    client = TestClient(app)

    # Тест GET /products
    response = client.get("/products")
    assert response.status_code == 200
    print("GET /products: OK")

    # Тест GET /products/{id}
    response = client.get("/products/1")
    assert response.status_code == 200
    print("GET /products/1: OK")

    # Тест POST /orders
    response = client.post("/orders", json={"user_id": 1, "products": [[1, 1], [2, 5]]})
    assert response.status_code == 201
    print("POST /orders: OK")

    # Тест PUT /products/{id}
    response = client.put("/products/1", json={"name": "Ноутбук", "price": 125489})
    assert response.status_code == 200
    print("PUT /products: OK")

    # Тест DELETE /products/{id}
    response = client.delete("/products/7")
    assert response.status_code == 200
    print("DELETE /products: OK")

    # Тест GET /users
    response = client.get("/users")
    assert response.status_code == 200
    print("GET /users: OK")

    # Тест GET /users/{id}
    response = client.get("/users/1")
    assert response.status_code == 200
    print("GET /users/1: OK")

    # Тест POST /users
    response = client.post("/users", json={"name": "Alex", "email": "alex@mail.ru"})
    assert response.status_code == 201
    print("POST /users: OK")

if __name__ == "__main__":
    test_api()