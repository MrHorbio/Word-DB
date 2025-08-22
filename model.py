from pydantic import BaseModel



class add_word(BaseModel):
    word:str
    meaning:str