import pytesseract
from PIL import Image
import csv
import os

def image_to_csv(image_path):
    """
    Convert an image of a table to a CSV file and save it in the specified folder.
    
    Parameters:
        image_path (str): Path to the input image file.
        output_folder (str): Path to the output folder where the CSV will be saved.
    """
    
    # Extract the base name of the image file (without extension) for naming the CSV
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    output_csv_path = os.path.join("output", f"{image_name}.csv")
    
    # Load the image
    image = Image.open(image_path)
    
    # Extract text from the image using OCR
    extracted_text = pytesseract.image_to_string(image)
    
    # Split the text into lines
    lines = extracted_text.splitlines()
    
    # Define headers for the CSV
    header = ["ref", "partnumber", "partname", "qty"]
    rows = []
    
    for line in lines:
        # Split line into words (adjust delimiter if needed)
        columns = line.split()
        
        # Ensure the line has enough columns to process
        if len(columns) >= 4:
            # Extract columns based on position
            ref = columns[0]  # First column as ref (string)
            partnumber = columns[1]  # Second column as partnumber (string)
            partname = " ".join(columns[2:-1]).replace("|", "").strip()  # Join middle columns as partname and clean unwanted characters
            try:
                qty = int(columns[-1])  # Last column as qty (integer)
            except ValueError:
                continue  # Skip rows where qty is not an integer
            
            # Append the row to the list
            rows.append([ref, partnumber, partname, qty])
    
    # Write data to a CSV file
    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write header
        writer.writerows(rows)  # Write rows
    
    print(f"CSV file has been created at: {output_csv_path}")

# Example usage:
# Replace 'input_image.png' with the path to your image file
image_to_csv("img/Screenshot_20241119_135837.png")
