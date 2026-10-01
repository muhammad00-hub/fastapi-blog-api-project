from database import Base

from sqlalchemy import Column,Integer,String,Text

class Blog(Base):

    __tablename__ = "blogs"

    id = Column(Integer,primary_key=True,index=True)

    title = Column(String)

    content = Column(Text)

