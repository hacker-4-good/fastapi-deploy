from fastapi import FastAPI, Request, Form, status
from fastapi.templating import Jinja2Templates 
from fastapi.responses import RedirectResponse 
from fastapi.middleware.cors import CORSMiddleware
import joblib

app = FastAPI() 

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/submit")
async def submit(request: Request, temperature: float = Form(...), humidity: float = Form(...)):
    model = joblib.load("model.pt")
    pred = model.predict([[temperature, humidity]])[0]
    response = RedirectResponse(url=request.url_for("details"), status_code=status.HTTP_303_SEE_OTHER)
    if pred>0.5:
        response.set_cookie("rainfall", "Yes")
    else:
        response.set_cookie("rainfall", "No")
    return response

@app.get("/details")
async def details(request: Request):
    prediction = request.cookies.get("rainfall")
    return templates.TemplateResponse("details.html", {"request": request, "prediction": prediction})