
import pytesseract
from PIL import Image
import pandas as pd 

# Open the .jpeg file using the PIL library
image = Image.open('/Users/vamsi/Downloads/IMG_D5A080012F56-1.jpeg')

# Use pytesseract to scan the text from the image
text = pytesseract.image_to_string(image)

# Print out the scanned text
print(text)

df = pd.DataFrame(text)
print(df)