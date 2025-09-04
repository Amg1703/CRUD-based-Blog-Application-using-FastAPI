from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
from schemas import BlogSchemaModel, BlogSchemaResponseModel
import models
from models import BlogDatabaseModel
from database import Base, engine, local_session
from sqlalchemy.orm import Session, query
from typing import Dict
app=FastAPI()

# THIS LINE IS RAN EVERY TIME WE RUN THE MAIN.PY FILE THIS LINE IS USED TO CREATE THE TABLE FOR MODELS OR TABLE AND COLUMNS WRITTEN IN THE DATABASE
models.Base.metadata.create_all(bind=engine)
# IF THIS LINE IS ALREADY RUN AND THE DATABASE TABLE IS ALREADY CREATED THEN IT WONT MAKE DIFFERENCE 

def get_db():
    db=local_session()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog/", response_model=BlogSchemaModel)
# SO WE DONT USE GET_DB() AS ELSE FASTAPI WILL IMMEDIATELY CALL THE FUNCTION WHEREAS WE ONLY NEED IT TO BE CALLED ONLY WHEN THE ENDPOINT IS CALLED SO FASTAPI INJECTS THIS DEPENDENCY USING THE DEPENDS FUNCTION
def create_blog(request:BlogSchemaModel, db:Session=Depends(get_db)):
    new_blog=models.BlogDatabaseModel(blog_title=request.blog_title, blog_body=request.blog_body) # THE PARAMETERS NAMES ARE SUPPOSED TO MATCH
    # WITH THE ACTUAL NAMES OF THE TABLE PRESENT IN THE DATABASE
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def get_db():
    db=local_session()
    try:
        yield db
    finally:
        db.close

# IF YOU WANT TO FETCH ALL THE DATA FROM THE DATABASE USE DB.QUERY(MODELS_FILENAME.DATABASE_MODEL_NAME).ALL() IF YOU WANT FETCH ALL THE DATA FROM THE DATABASE
@app.get("/getallblogs/")
def get_all_blogs_available(db:Session=Depends(get_db)):
    all_blogs=db.query(models.BlogDatabaseModel).all()
    return all_blogs

# IF YOU WANT TO FETCH DATA FROM THE DATABASE USING A PARAMETER SAY ID THEN USE db.query(model_filename.database_modelname).filter(table_name_you want_filter_based_on)
@app.get("/blogsby{id}/")
def get_blogs_by_id(id:int, db:Session=Depends(get_db),):
    blog_of_id=db.query(models.BlogDatabaseModel).filter(models.BlogDatabaseModel.id==id).first() # SO SQLALCHEMY RETURNS THE WHOLE DATABASE SO WE USE FIRST() SO ONLY THE FIRST RESPONSE IS SHOWN
    return blog_of_id 


# IF YOU HANDLE EXCEPTION CASES WHERE THE DATA IS NOT PRESENT IN THE DATABASE OR THE OPERATION CANNOT BE DONE WE CAN DO SO USING STATUS CODES
# WHEN YOU ARE CREATING SOMETHING BY PROTOCOL THE SERVER SHOULD RETURN THE STATUS CODE OF 201 
# BUT WE DONT HAVE TO REMEMBER THE STATUS CODE JUST IMPORT STATUS FROM FASTAPI AND USE THE PARAMETER status_code=status.AND JUST TYPE YOUR OPERATION AND FASTAPI WILL FIND THE STATUS CODE FOR YOU
@app.post("/createnewblog/",status_code=status.HTTP_201_CREATED)
def create_new_blog(request:BlogSchemaModel, db: Session=Depends(get_db)):
    new_blog=models.BlogDatabaseModel(blog_title=request.blog_title, blog_body=request.blog_body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# IF AN ERROR IS THROWN WE CAN USE THE RESPONSE METHOD OR THE HTTPEXCEPTION
# RESPONSE METHOD - Import Response FROM FastAPI
@app.get("/getblogsbytitle/{blog_title}", status_code=status.HTTP_200_OK)
def get_blogs_by_title(blog_title:str, response: Response,db: Session=Depends(get_db)):
    fetched_blog=db.query(models.BlogDatabaseModel).filter(models.BlogDatabaseModel.blog_title==blog_title).first()
    if not fetched_blog:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {"detail":f"The blog article for the title - {blog_title} is not available"}
    return fetched_blog

# HTTPEXCEPTION METHOD - IMPORT HttpException from FastAPI 
@app.get("/getblogsbyid/{blog_id}")
def get_blogs_by_id(blog_id:int, db: Session=Depends(get_db)):
    fetched_blog=db.query(models.BlogDatabaseModel).filter(models.BlogDatabaseModel.id==blog_id).first()
    if not fetched_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog article for the id number {blog_id} is not available")
    return fetched_blog

@app.delete("/deleteblog/{blog_id}")
def delete_blog(blog_id: int, db:Session=Depends(get_db)):
    db.query(models.BlogDatabaseModel).filter(models.BlogDatabaseModel.id==blog_id).delete(synchronize_session=False)
    db.commit()
    return {f"The blog with the id {blog_id} has been deleted"} 

@app.put("/updateblog/{blog_id}")
def update_blog(blog_id: int, request:BlogSchemaModel,db:Session=Depends(get_db)):
    # LETS CREATE AN INSTANCE OF THIS FUNCTION SO THAT WE DONT WE CAN USE IT FOR IF ELSE STATEMENTS 
    blog_to_be_updated=db.query(models.BlogDatabaseModel).filter(models.BlogDatabaseModel.id==blog_id)
    if blog_to_be_updated.first():
        blog_to_be_updated.update(request.dict(), synchronize_session=False)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with mentioned blog id {blog_id} was not found")
    db.commit()
    return {f"The blog with the blog id {blog_id} was updated"}


@app.delete("/deleteblogafterchecking/{blog_id}")
def delete_blog_after_checking(blog_id: int,db:Session=Depends(get_db)):
    blog_to_be_deleted=db.query(models.BlogDatabaseModel).filter(models.BlogDatabaseModel.id==blog_id)
    if blog_to_be_deleted.first():
        blog_to_be_deleted.delete(synchronize_session=False)
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.commit()
    return {f"The blog with the id {blog_id} is deleted successfully"}

# def get_db():
#     db=local_session()
#     try:
#         yield db
#     finally:
#         db.close

# SO WE CAN ENTER THE RESPONSE MODEL OR SCHEMA WE ARE EXPECTING WHILE DEFINING THE API 
@app.get("/blogsbyidpractice/{blog_id}", status_code=status.HTTP_200_OK, response_model=BlogSchemaResponseModel)
def get_blogs_by_id_practice(blog_id: int, db:Session=Depends(get_db)):
    get_blog_available=db.query(models.BlogDatabaseModel).filter(models.BlogDatabaseModel.id==blog_id)
    if get_blog_available.first():
        return get_blog_available.first()
    else:
        return HTTPException(staus_code=status.HTTP_404_NOT_FOUND, details=f"The blog for the given id of {blog_id} is not available")

