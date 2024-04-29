from fastapi import FastAPI, UploadFile, File #( web framework for building APIs )
from io import BytesIO #(BytesIO is a class from the io module that provides an in-memory stream for binary data)
import hashlib #(module in Python provides secure hash and message digest algorithms)
from PIL import Image #(Python Imaging Library that adds image processing capabilities to Python interpreter)
import imagehash #(Python library for computing perceptual image hashes. )

def hash_image(image_data):
    if not isinstance(image_data, bytes):
        image_data = image_data.read() 

    hash_value = hashlib.sha256(image_data).hexdigest()
    return hash_value


def getPHash(inputImage):
    image = Image.open(inputImage)
    phash = imagehash.phash(image)
    return phash


def getDHash(inputImage):
    image = Image.open(inputImage)
    dhash = imagehash.dhash(image)
    return dhash


app = FastAPI()


@app.get("/")
def hello():
    return {"Hello": "World"}


@app.post("/phash")
async def calculate_phash(image: UploadFile = File(...)):
    contents = await image.read()
    phash = getPHash(BytesIO(contents))
    return {"phash": str(phash)}


@app.post("/dhash")
async def calculate_dhash(image: UploadFile = File(...)):
    contents = await image.read()
    dhash = getDHash(BytesIO(contents))
    return {"dhash": str(dhash)}



@app.post("/cryptographic-hash")
async def cryptographic_hash(image: UploadFile = File(...)):
    if isinstance(image.content_type, str) and image.content_type.startswith("image/"):
        contents = await image.read()
        hashId = hash_image(contents)
        return {"hashId": hashId}
    else:
        return {"error": "Only image uploads are supported"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)