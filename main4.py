from fastapi import FastAPI, Path, Query 
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

class New_Flavour(BaseModel):
    Flavour: str 
    Quantity: float
    Availability : str
    Type: Optional[str] =None
    
class Update_Flavour(BaseModel):
    Flavour: Optional[str] = None 
    Quantity: Optional[float] = None
    Availability : Optional[str] = None
    Type: Optional[str] =None
    

inventory ={
            1: {"Flavour": "Vanilla",
                "Quantity":"30 Litres a week",
                "Availability": " Served all year round",
                "Type": "Vegan options available"      
                 },
            2: {"Flavour":"Choc Mint",
                "Quantity":"20Litres a week",
                "Availability": " Served all year round",
                "Type": "Vegan option not available"      
                 },
            3: {"Flavour": "Chocolate",
                "Quantity":"25 Litres a week",
                "Availability": " Served all year round",
                "Type": "Vegan options available",      
                 },                 
            4: {"Flavour": "Strawberry",
                "Quantity":"25 Litres a week",
                "Availability": " Served all year round",
                "Type": "Vegan options available",      
                 }

            }
pricing = {
    "small": 5, 
    "regular": 8,
    "large": 12

}

@app.get("/")
def homepage ():
    return {"Welcome to Angie's icecream palour"}

@app.get("/about")
def details ():
    return {"The palor is open: Monday - Friday from 1100hrs - 1500hrs. Weekends - 1100hrs - 1700hrs. Address: 5 Mountview Avenue" }


@app.get("/get-inventory/{flavour_details}") #will need to put a limitation to this
def get_inventory(flavour_details:int = Path (None, description = "insert a number id to get details of the inventory", gt=0, lt=5 )):
    return inventory [flavour_details]

@app.get("/get-by-flavour") #will need to put a limitation to this
def get_inventory(flavour: Optional[str]= None ):
    for flavour_details in inventory:
        if inventory[flavour_details]["flavour"] == flavour:
            return inventory[flavour_details]
    return{"Data":"Not found"}

@app.get("/get-prices/{size_pricing}")
def get_prices(size_pricing:str = Path (None, description = "insert a size (small/regular/large) to get the price ")):
    return pricing [size_pricing]

@app.post("/create-flavour/{flavour_id}")
def create_flavour(flavour_id:int, flavour: New_Flavour):
    if flavour_id in inventory:
        return{"Error": "This flavour exists."}

    inventory[flavour_id] = {"Flavour" :flavour.Flavour, "Quantity":flavour.Quantity, "Availability":flavour.Availability, "Type":flavour.Type}
    return inventory[flavour_id]

@app.put("/update-item/{flavour_id}")
def update_item (flavour_id:int, flavour: Update_Flavour):
    if flavour_id not in inventory:
        return{"Error": "This flavour does not exists."}
    
    if flavour.Flavour!= None:
        inventory[flavour_id].Flavour = flavour.Flavour
    
    if flavour.Quantity!= None:
        inventory[flavour_id].Quantity = flavour.Quantity

    if flavour.Availability!= None:
        inventory[flavour_id].Availability = flavour.Availability

    if flavour.Type!= None:
        inventory[flavour_id].Type = flavour.Type

    return inventory[flavour_id]

@app.delete("/delete-item")
def delete_item(flavour_id: int =  Query(..., description = "The id of the flavour to delete", gt=0)):
    if flavour_id not in inventory:
        return{"Error":" ID does not exist."}
    
    del inventory[flavour_id]
    return{"Success":"Item deleted"}
