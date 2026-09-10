from fastapi import APIRouter

from app.api.v1.endpoints import auth, clauses, cost_estimate, dashboard, rules, seat_allocation, seats

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(dashboard.router)
api_router.include_router(seats.router)
api_router.include_router(rules.router)
api_router.include_router(seat_allocation.router)
api_router.include_router(clauses.router)
api_router.include_router(cost_estimate.router)
