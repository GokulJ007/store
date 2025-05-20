from fastapi import FastAPI,HTTPException
from connected import DB_connection
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 Allow all origins (good for local dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/home")
def demo():
    connect=DB_connection()
    cursor=connect.cursor()
    cursor.execute("""select * from products""")
    data=cursor.fetchall()
    return data
 
@app.get("/prodisplay")
def prodisplay(category:str = None):
    connect=DB_connection()
    cursor=connect.cursor()
    if category:
        cursor.execute("select * from products where category=%s",(category,))
    else:
        cursor.execute("select * from products")
    data=cursor.fetchall()
    return data

class products(BaseModel):    
    name:str
    description:str
    price:int
    image_url:str
    category:str
@app.post("/insertpro")
def insertpro(pro:products):
    try:
        connect=DB_connection()
        cursor=connect.cursor()
        query="""insert into products(name,description,price,image_url,category) values(%s,%s,%s,%s,%s) """
        cursor.execute(query,(
            pro.name,
            pro.description,
            pro.price,
            pro.image_url,
            pro.category
        ))
        connect.commit()
        return{"message":"Data  added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


