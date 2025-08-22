from fastapi import FastAPI,HTTPException,Query
from model import add_word
from db import collection
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

app = FastAPI()

# Helper to convert Mongo ObjectId
def word_helper(word) -> dict:
    return {
        "id": str(word["_id"]),
        "word": word["word"],
        "meaning": word["meaning"],
    }


app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],
     allow_headers=["*"],
     allow_credentials=True,
     allow_methods=["*"],
)



@app.post("/add")
async def add(data:add_word):
     # Check if word already exists
    existing = await collection.find_one({"word": data.word})
    if existing:
        raise HTTPException(status_code=400, detail="Word already exists")
    
    payload = {
        "word" : data.word,
        "meaning": data.meaning
    }

    addition = await collection.insert_one(payload)
    return {"message":"Added successfully", "id": str(addition.inserted_id)}
    
@app.get("/find")
async def find(word: str = Query(...)):
    # Case-insensitive exact match
    doc = await collection.find_one({"word": {"$regex": f"^{word}$", "$options": "i"}})

    if not doc:
        raise HTTPException(status_code=404, detail="Word not found")

    doc["_id"] = str(doc["_id"])  # Convert ObjectId
    return {"_id": doc["_id"], "word": doc["word"], "meaning": doc["meaning"]}

@app.get("/all")
async def get_all_words():
    words = []
    cursor = collection.find({})
    async for doc in cursor:
        doc["id"] = str(doc["_id"]) 
        del doc["_id"]
        words.append(doc)  

    return words  
         
         
         