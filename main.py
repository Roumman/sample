from enum import Enum
from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Модели и типы
class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


class ValidationError(BaseModel):
    loc: List[str]
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    detail: Optional[List[ValidationError]]


# База данных
dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


# Роуты
@app.get('/')
def root():
    return {"message": "Welcome to FastAPI!"}


@app.post('/post', response_model=Timestamp)
def get_post():
    if post_db:
        return post_db[-1]
    raise HTTPException(status_code=404, detail="No posts found")


@app.get('/dog', response_model=List[Dog])
def get_dogs(kind: Optional[DogType] = Query(None)):
    if kind:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    return list(dogs_db.values())


@app.post('/dog', response_model=Dog)
def create_dog(dog: Dog):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=400, detail="Dog with this pk already exists")
    dogs_db[dog.pk] = dog
    return dog


@app.get('/dog/{pk}', response_model=Dog)
def get_dog_by_pk(pk: int = Path(..., description="Primary key of the dog")):
    if pk in dogs_db:
        return dogs_db[pk]
    raise HTTPException(status_code=404, detail="Dog not found")


@app.patch('/dog/{pk}', response_model=Dog)
def update_dog(pk: int, dog: Dog):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    dogs_db[pk] = dog
    return dog
