from fastapi import FastAPI

server = FastAPI()

list = []

@server.get("/")
def root():
    return{"Names": list}

@server.get("/insert/{name}")
def inserting(name: str):
    list.append(name)
    return {"message": f"{name} added to the list!"}

@server.get("/remove/{name}")
def removing(name: str):
    if name in list:
        list.remove(name)
        return {"message": f"{name} removed from the list!"}
    else:
         return {"message": f"{name} not found in the list."}