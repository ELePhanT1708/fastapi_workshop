from fastapi import FastAPI
from .api import router


tags_metadata = [
    {
        'name': 'auth',
        'description': 'Авторизация и регистрация пользователя'
    },
    {
        'name': 'operations',
        'description': 'Работа с операциями'
    },
    {
        'name': 'reports',
        'description': 'Импорт и экспорт отчетов'
    }
]


app = FastAPI(
    title='Workshop',
    description='Сервис учета доходов и расходов',
    version='1.0.0',
    openapi_tags=tags_metadata
)
app.include_router(router)


@app.get('/')
def root():
    return {'message': 'Hello world!'}
