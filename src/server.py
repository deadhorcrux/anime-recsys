

import pickle
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class MyCustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "__main__":
            module = "similitary"
        return super().find_class(module, name)

class Title(BaseModel):
    title: str


@app.post('/predict')
def predict(title: str):
    prediction = model.predict(title)
    return prediction
    

with open('similitary.pkl', 'rb') as f:
    unpickler = MyCustomUnpickler(f)
    model = unpickler.load() 

if __name__ == '__main__':
    model.predict('Наруто')
    uvicorn.run(app, host='127.0.0.1', port=8000)
