from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/dashboard")

@router.get("/stats")
async def get_dashboard_stats():
    return JSONResponse(content={
        "totalProducts": 120,
        "lowStockProducts": 8,
        "pendingDeliveries": 15,
        "productOutput": 40,
        "totalProductsTrend": "+5%",
        "lowStockProductsTrend": "-2%",
        "pendingDeliveriesTrend": "+10%",
        "productOutputTrend": "-3%",
    })