from fastapi import FastAPI,HTTPException,Path
from connected import DB_connection
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from fastapi import Query
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


# Define a route that handles GET requests to /prodisplay
# Optionally accepts a category as a query parameter (?category=men)
@app.get("/prodisplay")
def prodisplay(category:str=Query(None)):
    connect=DB_connection()
    cursor=connect.cursor()
    if category:
        cursor.execute("SELECT * FROM products WHERE category=%s", (category,))
    else:
        print("some worng")
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


@app.put("/updatepro/{id}")
def updatepro(id:int=Path(...),pro:products=None):
    try:
        connect=DB_connection()
        cursor=connect.cursor()
        update_query="""
        update products 
        set name=%s,description=%s,price=%s,image_url=%s,category=%s where id=%s"""
        cursor.execute( update_query,(
            pro.name,
            pro.description,
            pro.price,
            pro.image_url,
            pro.category,
            id
        ))
        connect.commit()
        return{"message":"updated sucessfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/deletepro/{id}")
def deletepro(id:int):
    try:
        connect=DB_connection()
        cursor=connect.cursor()
        cursor.execute("delete from products where id=%s;",(id,))
        connect.commit()
        return{"message":"deleted sucssesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#add to cart

# @app.post("/addtocart")
# def addtocart(item:cart):
#     try:
#         connect=DB_connection()
#         cursor=connect.cursor()
#         cursor.execute("select * from products where id=%s",(item.product_id,))
#         product=cursor.fetchone()
#         if not product:
#             raise HTTPException(status_code=404,detail="product not found")
        
#         cursor.execute("select * from cart where product_id=%s",(item.product_id,))
#         exist=cursor.fetchone()
#         if exist:
#             raise HTTPException(status_code=400,detail="product already in cart")

#         cursor.execute("insert into cart (product_id,quantity) values(%s,%s)",
#         (item.product_id,item.quantity)
#         )
#         connect.commit()
#         return{"message":"product added to cart"}
#     except Exception as e:
#         print("Error in /addtocart:", e)
#         raise HTTPException(status_code=500,detail=str(e))


class cart2(BaseModel):
    product_id:int
    quantity:int
    size:Optional[str] = None # Unified cart model: handles both sized and non-sized products by making 'size' optional
@app.post("/detailed_add_to_cart")
def detailed_add_to_cart(item:cart2):
    try:
        connect=DB_connection()
        cursor=connect.cursor()
        cursor.execute("select * from products where id=%s",(item.product_id,))
        product=cursor.fetchone()
        
        if not product:
            raise HTTPException(status_code=404,detail="product not found")
        cursor.execute("select * from cart where product_id=%s and size=%s",(item.product_id,item.size,))
        exist=cursor.fetchone()  
        if exist:
            raise HTTPException(status_code=400,detail="product with this already in cart")
        
        cursor.execute("insert into cart (product_id, quantity, size) values(%s,%s,%s)",(item.product_id,item.quantity,item.size))
        connect.commit()

        return{"message":"product added with size succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

    
@app.get("/cart")
def get_items():
    try:
        connect=DB_connection()
        cursor = connect.cursor()
        cursor.execute("""select 
        cart.id as cart_id,
        cart.product_id,
        products.name,
        products.description,
        products.price,
        products.image_url,
        cart.quantity,
        cart.size
        from cart join products on cart.product_id=products.id;
        """)
        data=cursor.fetchall()# Fetch all results as a list of dictionaries
        return data
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@app.delete("/delete_cart_item/{product_id}")
def delete_cart_item(product_id:int):
    try:
        connect=DB_connection()
        cursor=connect.cursor()
        cursor.execute("delete from cart where product_id=%s",(product_id,))
        connect.commit()
        return {"message":"product removed succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@app.put("/update_quantity")
def update_quantity(item:cart2):
    try:
        connect=DB_connection()
        cursor=connect.cursor()
        cursor.execute("update cart set quantity=%s where product_id=%s",(item.quantity,item.product_id,))
        connect.commit()
        return {"message": "Quantity updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@app.get("/prodeatil/{id}")
def prodeatil(id:int):
    try:
        connect=DB_connection()
        cursor=connect.cursor()
        cursor.execute("select * from products where id=%s",(id,))
        data=cursor.fetchone()
        return data
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@app.get("/getcart")
def getcart():
    try:
        connect=DB_connection()
        cursor=connect.cursor()
        cursor.execute("select * from cart")
        data=cursor.fetchall()
        return data
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@app.get("/searchapi")
def searchapi(category:str=Query(None),name:str=Query(None)):
    try:
        connect=DB_connection()
        cursor=connect.cursor()
        if category and name:
            cursor.execute("select * from products where category=%s and name=%s",(category,name,))
        elif category:
            cursor.execute("select * from products where category=%s",(category,))
        elif name:
            cursor.execute("select * from products where  name=%s",(name,))
        else:
            cursor.execute("select * from products")
        data=cursor.fetchall()
        return data
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

