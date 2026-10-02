from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.attendance import router as attendance_router
from app.routers.auth import router as auth_router
from app.routers.chefs import router as chefs_router
from app.routers.jobs import router as jobs_router
from app.routers.payroll import router as payroll_router
from app.routers.users import router as users_router
from app.routers.workers import router as workers_router

app = FastAPI()


app.include_router(users_router)
app.include_router(jobs_router)
app.include_router(workers_router)
app.include_router(attendance_router)
app.include_router(payroll_router)
app.include_router(auth_router)
app.include_router(chefs_router)

app.add_middleware( CORSMiddleware, allow_origins=[ "http://127.0.0.1:5500", "http://localhost:5500", ], allow_credentials=True, allow_methods=["*"], allow_headers=["*"], ) # باقي routers # app.include_router(...)