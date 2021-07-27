from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.extract_content import EmailContent

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def main(request: Request):

    await json()

    return templates.TemplateResponse(
        'index.html',
        {
            'request': request
        })


@app.get('/json')
async def json():
    emailContent = EmailContent()

    content = emailContent.extractContent()

    return content
