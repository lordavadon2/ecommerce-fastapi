from fastapi import FastAPI
from ecommerce.user import router as user_router

app = FastAPI(title='EcommerceApp',
              version='0.0.1')

app.include_router(user_router.router)


