from fastapi import FastAPI, Depends,HTTPException
app=FastAPI()

@app.get("/")
async def demo():
   return {"message": "VASANTHAN_WORK"}

from sqlalchemy import create_engine
from sqlalchemy.engine import url
from sqlalchemy.orm import sessionmaker

url_demo="sqlite:///./demo.db"
engine=create_engine(url_demo)
Session=sessionmaker(engine)
session=Session()

from sqlalchemy import Column,INTEGER,String,BOOLEAN,Integer,Boolean
from sqlalchemy.orm import declarative_base
base=declarative_base()

class task(base):
    __tablename__="Tasks"
    id=Column(Integer,primary_key=True,unique=True)
    title=Column(String)
    description =Column(String)
    completed=Column(Boolean,default=False)
base.metadata.create_all(engine)

def depend():
    session = Session()
    try:
        yield session
    finally:
        session.close()
        
# create the task
@app.post("/create_task")
def add_task(title:str,description:str,completed:bool,session:Session=Depends(depend)):
    t1=task(title=title,description=description,completed=completed)
    session.add(t1)
    session.commit()
    return {"tasks":t1.id}

# read the task
@app.get("/read_task/{id}")
def display_task(id:int,session:Session=Depends(depend)):
    t1= session.query(task).filter(task.id==id).first()
    if t1 is None:
        raise HTTPException(404,"id is not found")
    return t1

# update the task
@app.put("/update_task/{id}")
def update_task( id: int, new_title: str="", new_description:str="",new_completed : bool=False,session:Session=Depends(depend)):
   # t1=task(id=id,title=new_title,description=new_decr,completed=new_comp)
    t1= session.query(task).filter(task.id==id).first() 
    t1.id=id
    t1.title =new_title 
    t1.description=new_description
    t1.completed = new_completed
    session.add(t1)
    session.commit()
    return {"tasks":t1.id}

# delete the task
@app.delete("/delete_task/{id}")
def delete_task(id:int,session:Session=Depends(depend)):
    t1=session.query(task).filter(task.id==id).first()
    if t1 is None:
        raise HTTPException(404,"id is not found")
    session.delete(t1)
    session.commit()
    return {"task":t1.id}

#display all the list of tasks
@app.get("/display_all_tasks")
def display_all_tasks(session:Session=Depends(depend)):
    t1= session.query(task).all()
    return t1

# display the completed tasks
@app.get("/display_completed_tasks")
def display_completed_tasks(session:Session=Depends(depend)):
    t1=session.query(task).filter(task.completed==True).all()
    return t1
