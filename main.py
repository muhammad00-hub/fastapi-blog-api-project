from fastapi import FastAPI , Depends, HTTPException,Query

from sqlalchemy.orm import Session

from database import engine, Sessionlocal

import model, schema

from auth import verify_token, create_token

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login")

def login():
    return  {
        "access_token":create_token({"user":"admin"}),
        "token_type":"bearer"
    }


@app.get("/")

def home():
    return {"message":"This is my home page"}

@app.post("/blogs",response_model=schema.BlogResponse )

def create_blog(blog:schema.BlogCreate,db:Session=Depends(get_db), user=Depends(verify_token)):

    new_blog = model.Blog(
        title = blog.title ,

        content = blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return  new_blog

@app.get("/blogs")

def read_blogs( page:int=1,limit:int=5,search:str=Query(default=""),db:Session=Depends(get_db)):

    query = db.query(model.Blog)
    if search:
        query = query.filter(model.Blog.title.like(f"%{search}%"))
    total = query.count()
    start = (page-1)*limit
    blogs = query.offset(start).limit(limit).all()

    return {
        "page":page,
        "limit":limit,
        "total":total,
        "data":blogs
    }
 

@app.get("/blogs/{id}",response_model= schema.BlogResponse)

def read_blog(id:int,db:Session=Depends(get_db)):

    blog = db.query(model.Blog).filter(model.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code = 404, detail=f"Blog is not found with the id{id}")
    return blog 


@app.put("/blogs/{id}",response_model= schema.BlogResponse)

def update_blog(id:int,blog:schema.BlogCreate,db:Session=Depends(get_db), user=Depends(verify_token)):

    blog_exist = db.query(model.Blog).filter(model.Blog.id == id).first()
    
    if not blog_exist:
        raise HTTPException(status_code = 404, detail=f"Blog is not found with the id{id}")
    blog_exist.title = blog.title
    blog_exist.content = blog.content
    db.commit()
    
    return blog_exist     

@app.delete("/blogs/{id}")
def delete_blog(id: int, db: Session = Depends(get_db),user=Depends(verify_token)):

    blog = db.query(model.Blog).filter(model.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=404,
            detail=f"Blog is not found with the id {id}"
        )

    db.delete(blog)
    db.commit()

    return {
        "Message": f"Blog with the id {id} is deleted successfully."
    }

