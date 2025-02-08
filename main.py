import os
import fitz
import pytesseract
import cv2
import io
from PIL import Image, ImageFile
from colorama import Fore, init
import platform

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Global var
strPDF, textScanned,  textScanned, inputTeEx, dirName = "","","","", ["images", "output_txt"]

# Get input from User
def gInUs():
    # Global var
    global strPDF
    global inputTeEx

# ... existing code ...
    if(platform.system() == "Windows"):
        inputTeEx = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        print(Fore.GREEN + "[!] Using Tesseract from: " + inputTeEx + Fore.RESET)
# ... existing code ...

    # Print input
    base_path = r"C:\Users\hexza\teseract\upload"
    print(Fore.GREEN + "[!] Insert filename of PDF in upload folder:" + Fore.RESET)
    inputUser = input()
    full_path = os.path.join(base_path, inputUser)
    
    # Print an alert if input is not valid, if not, call to fun reDoc
    if(inputUser == ""):
        print(Fore.RED + "[X] Please enter a valid filename" + Fore.RESET)
    else:
        extIm(full_path)
    # -------------


# Extracting images
def extIm(fileStr):
    global dirName

    # open the file
    pdf_file = fitz.open(fileStr)

    # Create output folder if don't exists
    for i in dirName:
        try:
            os.makedirs(i)
            print(Fore.GREEN + "[!] Directory " , i ,  " Created"+ Fore.RESET)
        except FileExistsError:
            print(Fore.RED + "[X] Directory " , i ,  " already exists" + Fore.RESET)

    # List images if exists and print each one. if not extract all images uWu
    content = os.listdir("images")
    if(len(content) >= 1):
        # Print every img in content
        for i in content:
            print(Fore.YELLOW + f"This is an image: {i}" + Fore.RESET)
    else:
        # Iterate over PDF pages
        for page_index in range(len(pdf_file)):
            # get the page itself
            page = pdf_file[page_index]
            image_list = page.get_images()

            # printing number of images found in this page
            if image_list:
                print(Fore.GREEN + f"[+] Found a total of {len(image_list)} images in page {page_index}" + Fore.RESET)
            else:
                print(Fore.RED + "[!] No images found on page", page_index, Fore.RESET)

            for (image_index, img) in enumerate(image_list, start=1):
                # get the XREF of the image
                xref = img[0]
                # extract the image bytes
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                # get the image extension
                image_ext = base_image["ext"]
                # load it to PIL
                image = Image.open(io.BytesIO(image_bytes))
                # save it to local disk
                image.save(open(f"images/image{page_index+1}_{image_index}.{image_ext}", "wb"))
    reImg()

def reImg():
    # Global var
    global textScanned
    global dirName
    global inputTeEx

    pytesseract.pytesseract.tesseract_cmd = f"{inputTeEx}"

    # List the images
    content = os.listdir('images')

    for i in range(len(content)):
        # Reading each image in images
        image = cv2.imread(f'images/{content[i]}')

        # Scan text from image - changed language to Thai
        print(Fore.YELLOW + f"[.] Scan text from {content[i]}" + Fore.RESET)
        text = pytesseract.image_to_string(image, lang='tha')

        # Concate text scanned in a string
        textScanned += text

        # print
        print(Fore.GREEN + "[!] Finished scan text" + Fore.RESET)

        # Showing img input
        cv2.imshow('Image',image)
        # 0.5 milisecond
        cv2.waitKey(1000)

    # Create and write file txtResult.txt with UTF-8 encoding
    print(Fore.CYAN + "[.] Writing txtResult.txt" + Fore.RESET)
    fileTxt = open(f"{dirName[1]}/txtResult.txt", "w", encoding='utf-8')
    fileTxt.write(textScanned)
    fileTxt.close()
    print(Fore.GREEN + "[!] File Written" + Fore.RESET)
# Call to fun main
gInUs()