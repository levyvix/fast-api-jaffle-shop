from fastapi import FastAPI

from app import routers

app = FastAPI()

app.include_router(routers.customers_router)
app.include_router(routers.orders_router)
app.include_router(routers.item_router)
app.include_router(routers.product_router)
app.include_router(routers.supplies_router)
app.include_router(routers.store_router)


@app.get("/")
async def root():
    return {"message": "FastAPI Jaffle Shop!"}
