from typing import Union
import requests
import pandas as pd
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware



from fastapi import FastAPI

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="templates")
def getdata(startdate, enddate):
    try:
        url = 'https://api.nasa.gov/techtransfer'


        api_key = 'MTT4YSkdqTgXC9qoAYE56JIbHVUgUBpyrHKqgz1i'
        ur = f"https://api.nasa.gov/techtransfer/software/?DATA SERVERS PROCESSING AND HANDLING&api_key={api_key}"
        astro = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={startdate}&end_date={enddate}&api_key={api_key}"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',  # Adjust content type if needed
        }
        response = requests.get(astro)
        if response.status_code == 200:
            data = response.json()
            
            return data


        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(e)

@app.get("/{startdate}/{enddate}")
def read_root(startdate:str,enddate:str):
    data = getdata(startdate, enddate)
    # flat={}
    flat=data['near_earth_objects']
    output={}
    
    try:
        for key,value in flat.items():
            lis = []
            for val in value:
                
                lis.append(
                    {'Asteroids id': val['id'], 'Asteroids Name': val['name'], 'size': val['estimated_diameter'], 'learn More Nasa': val['nasa_jpl_url']})
                
                
            output[key] = lis
       
       
        
    except Exception as e:
        return {'error':e}
        
        
    # # single=data['results']
    # # columns = ['id']
    
    
    # try:
    #     df = pd.DataFrame(output)
    #     df=str(df.T)
    #     print(df)
    # except Exception as e:
    #     return {'error': e}
        
    # # zeroth_elements = [sublist[3] for sublist in single]
    # # df = pd.DataFrame(
    # #     zeroth_elements, columns=columns)
    # # return {'data': data}
    # dataa = {"key": df,"raw":output}
    # response = {"request": dataa}
    return output


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
