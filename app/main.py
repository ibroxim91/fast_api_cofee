from fastapi import FastAPI


app = FastAPI()

# Test endpoint
@app.get("/")
def read_test():
    return {"message": "Hello, World!"}
