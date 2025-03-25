from fastapi import FastAPI

from app import routers
from app.const import API_V1_PREFIX

app = FastAPI()

# api v1
app.include_router(routers.customers_router, prefix=API_V1_PREFIX)
app.include_router(routers.orders_router, prefix=API_V1_PREFIX)
app.include_router(routers.item_router, prefix=API_V1_PREFIX)
app.include_router(routers.product_router, prefix=API_V1_PREFIX)
app.include_router(routers.supplies_router, prefix=API_V1_PREFIX)
app.include_router(routers.store_router, prefix=API_V1_PREFIX)


@app.get("/")
async def root():
    return {"message": "FastAPI Jaffle Shop!"}
