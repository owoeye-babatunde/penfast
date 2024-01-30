from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from func import measure_length_width
import cv2
import numpy as np

app = FastAPI()

@app.post("/measure")
async def measure_image(file: UploadFile = File(...)):
    try:
        length, width = measure_length_width(file.file)
        return JSONResponse(content={"length": length, "width": width}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
