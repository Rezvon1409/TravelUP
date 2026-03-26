from fastapi import FastAPI
import uvicorn
from api.auth import router as auth_router
from api.profile import router as profile_router
from api.destinations import router as destinations_router
from api.bookings import router as bookings_router
from api.reviews import router as reviews_router
from api.payments import router as payments_router
from api.admin import router as admin_router



app = FastAPI(title="TravelUp")

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(destinations_router)
app.include_router(bookings_router)
app.include_router(reviews_router)
app.include_router(payments_router)
app.include_router(admin_router)


@app.get("/")
async def root():
    return {"msg": "TravelUp API is running!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)