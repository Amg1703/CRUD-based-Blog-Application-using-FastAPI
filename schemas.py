from pydantic import BaseModel, config

class BlogSchemaModel(BaseModel):
    blog_title: str
    blog_body: str

# SO THAT FASTAPI ACCEPTS ORM TYPE DATA WHEN FETCHING STORED DATA FROM THE DATABASE

class BlogSchemaResponseModel(BlogSchemaModel):
    blog_title: str
    # THE RESPONSE THE PYDANTIC MODEL NEEDS FROM THE DATABASE IS SUPPOSED TO BE DICTIONARY SO WE NEED USE CLAS CONFIG: ORM_MODE=TRUE TO LET THE ORM KNOW
    class config:
        orm_mode=True