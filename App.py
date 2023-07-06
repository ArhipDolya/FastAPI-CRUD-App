import uvicorn
from fastapi import FastAPI, Depends, Request
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session


Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app = FastAPI()

@app.get("/")
def root(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items

@app.get('/{id}')
def get_item_id(id: int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item

@app.post('/')
def add_item(item: schemas.Item, session: Session = Depends(get_session)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)

    return item

@app.put('/{id}')
def update_item(id: int, item: schemas.Item, session: Session=Depends(get_session)):
    item_obj = session.query(models.Item).get(id)
    item_obj.task = item.task
    session.commit()
    session.refresh(item_obj)

    return item_obj

@app.delete('/{id}')
def delete_item(id: int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    session.delete(item)
    session.commit()
    session.close()
    return {'message': 'Item deleted successfully'}


 # at last, the bottom of the file/module
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)