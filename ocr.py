# https://codetoprosper.com/extract-text-from-image-python
import pytesseract
import sys

file = sys.argv[1]
extracted_text = pytesseract.image_to_string(f'{file}.png')
with open(f'{file}.txt', 'w') as f:
  f.write(extracted_text)

# https://www.geeksforgeeks.org/how-to-remove-blank-lines-from-a-txt-file-in-python/
with open(f'{file}.txt', 'r') as r, open(f'{file}a.txt', 'w') as o:
    for line in r:
        if line.strip():
            o.write(line)