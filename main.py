from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
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


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # Open the image from the uploaded file
    image = Image.open(io.BytesIO(await file.read()))

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

    # Return the modified image
    return StreamingResponse(img_byte_arr, media_type="image/jpeg")

@app.get("/")
def root():
    return {"hello": 'world'}