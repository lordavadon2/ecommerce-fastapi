import uvicorn
from fastapi import FastAPI
from ecommerce.user import router as user_router
from ecommerce.cart import router as cart_router
from ecommerce.orders import router as order_router
from ecommerce.products import router

app = FastAPI(title='EcommerceApp',
              version='0.0.1',
              docs_url='/private_docs',
              redoc_url=None)

app.include_router(user_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)
app.include_router(router.category_router)
app.include_router(router.product_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
