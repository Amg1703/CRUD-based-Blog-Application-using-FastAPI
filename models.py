from database import Base
from sqlalchemy import Column, Integer, String

# THE NAMES OF THE TABLE ARE SUPPOSED TO BE THE SAME AS THE NAMES GIVEN IN THE SCHEMA

class BlogDatabaseModel(Base):
    __tablename__='Blogs'
    id=Column(Integer, primary_key=True, index=True)
    blog_title=Column(String)
    blog_body=Column(String)

    