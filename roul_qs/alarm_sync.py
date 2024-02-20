import pytesseract
from PIL import Image
import pandas as pd

# Open an image file
image = Image.open("roul_qs/static/IMG_1504.jpg")

# Perform OCR on the image
text = pytesseract.image_to_string(image)

# Split the text into lines
lines = text.split('\n')

# Create a DataFrame from the lines
df = pd.DataFrame({'Text': lines})

# Display the DataFrame
print(df)
