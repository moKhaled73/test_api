from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import base64
from PIL import Image, ImageEnhance
import io


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)


# Define a Pydantic model to accept base64-encoded image input
class ImageBase64Request(BaseModel):
    image_base64: str

@app.post("/upload-image/")
async def upload_image(image_data: ImageBase64Request):
    try:

        # Decode the base64 image
        image_data_str = image_data.image_base64.split(",")[1]  # Remove data URI scheme if present
        image_bytes = base64.b64decode(image_data_str)

        # Open the image from the decoded bytes
        image = Image.open(io.BytesIO(image_bytes))

        # Create a blue overlay
        blue_overlay = Image.new("RGBA", image.size, (0, 0, 255, 100))  # Semi-transparent blue

        # Convert image to RGBA if not already
        image = image.convert("RGBA")

        # Blend the blue overlay onto the image
        combined = Image.alpha_composite(image, blue_overlay)

        # Convert back to RGB (remove alpha)
        combined = combined.convert("RGB")

        # Save the image to a BytesIO object
        img_byte_arr = io.BytesIO()
        combined.save(img_byte_arr, format="JPEG")
        img_byte_arr.seek(0)

        # Convert the image to base64
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        # Add the data URI scheme to the base64 string
        img_base64 = f"data:image/jpeg;base64,{img_base64}"

        # Return the processed image as a base64 string with the data URI prefix
        return JSONResponse(content={"image_base64": img_base64})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/")
def root():
    return {"hello": 'world'}