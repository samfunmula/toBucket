from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from minio import Minio
from io import BytesIO
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/minIO/{image_name}")
async def get_image(image_name: str):
    try:
        bucket_name = "clip-images"
        object_name = f'/test/{image_name}'
        result = CLIENT.get_object(bucket_name, object_name)
        return StreamingResponse(BytesIO(result.data), media_type="image/png")
    except:
        return "Image not found", 404

@app.post("/get_bucket")
async def get_bucket(request : Request) -> JSONResponse:
    request = await request.json()
    
    bucket_name = "clip-images"
    object_folder = request.get('object_folder','')
    object_name = request.get('object_name',None)
    
    if not object_name:
        
        model_result = CLIENT.list_objects("clip-images",prefix=object_folder,use_url_encoding_type=True)
        for model in model_result:
            
            if model.object_name.startswith("score/All"):
                object_name = model.object_name
        
    else:
        object_name = request.get('object_name','')
        object_name = object_folder+object_name+".json"
        print(object_name)
    try:
        result = CLIENT.get_object(bucket_name, object_name)
        print(result)
        data = json.loads(result.data.decode('utf8').replace("'", '"'))
    except:
        return JSONResponse({"status":"get bucket error"}, status.HTTP_400_BAD_REQUEST)
    return data

@app.post("/save")
async def to_bucket(request : Request) -> JSONResponse:
    request = await request.json()
    category = request.get('category','')
    
    data_json = json.dumps(request)
    json_bytes = BytesIO(data_json.encode('utf-8'))

    bucket_name = "clip-images"
    object_name = f'/origin/{category}.json'
    try:
        CLIENT.put_object(bucket_name, object_name, json_bytes, len(data_json))
    except:
        return JSONResponse({"status":"save bucket error"}, status.HTTP_400_BAD_REQUEST)
    return {"status": "finish"}

if __name__ == "__main__":
    CLIENT = Minio(
        "heimdallr-minio.dev.cloud.biggo.com",
        access_key="jam@funmula.com",
        secret_key="Eec8eihe",
        secure=False
    )
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
