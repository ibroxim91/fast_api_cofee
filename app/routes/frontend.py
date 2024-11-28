from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

front_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@front_router.get("/admin/chat", response_class=HTMLResponse)
async def get_admin_chat():
    return templates.TemplateResponse("admin_chat.html", {"request": {}})

@front_router.get("/user/chat", response_class=HTMLResponse)
async def get_user_chat():
    return templates.TemplateResponse("user_chat.html", {"request": {}})
