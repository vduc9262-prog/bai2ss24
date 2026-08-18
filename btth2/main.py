from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from middleware.middleware import RBACMiddleware


app = FastAPI()


app.add_middleware(RBACMiddleware)




app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "https://driver.flashmove.io",
        "https://hub.flashmove.io"
    ],

    allow_methods=[
        "GET",
        "POST",
        "PATCH"
    ],

    allow_headers=[
        "Content-Type",
        "X-Role-Identity"
    ]
)




@app.post("/api/v1/orders/assign")
def assign_order():

    return {
        "status": "Success",
        "message": "Order assigned successfully"
    }



@app.patch("/api/v1/orders/status")
def update_order_status():

    return {
        "status": "Success",
        "message": "Order status updated successfully"
    }




@app.get("/api/v1/orders/track")
def track_order():

    return {
        "status": "Success",
        "message": "Order tracking information",
        "order_status": "IN_TRANSIT"
    }