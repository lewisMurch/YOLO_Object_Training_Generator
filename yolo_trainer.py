#Imports
import random
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter import StringVar
from tkinter import messagebox
import os.path

def overlay_image_with_bb_cropped(bg_img_path, overlay_img_path, save_img_path, num_repeats):
    # Open the background image
    bg_img = Image.open(bg_img_path)

    # Open the overlay image
    overlay_img = Image.open(overlay_img_path)

    # Get the width and height of the background image
    bg_width, bg_height = bg_img.size

    # Get the width and height of the overlay image
    overlay_width, overlay_height = overlay_img.size

    for i in range(num_repeats):
        # Generate random coordinates for the overlay image
        x = random.randint(0, bg_width - overlay_width)
        y = random.randint(0, bg_height - overlay_height)

        # Randomly decide whether to crop on the X or Y axis
        axis = random.choice(['X', 'Y'])

        if axis == 'X':
            # Generate a random crop on the X axis
            x_start = random.randint(0, overlay_width)
            x_end = x_start + overlay_width - 1
            overlay_img_cropped = overlay_img.crop((x_start, 0, x_end, overlay_height))
            
            # Update the bounding box information
            x += x_start
            overlay_width = overlay_img_cropped.width
        else:
            # Generate a random crop on the Y axis
            y_start = random.randint(0, overlay_height)
            
            y_end = y_start + overlay_height
            overlay_img_cropped = overlay_img.crop((0, y_start, overlay_width, y_end))

            # Update the bounding box information
            y += y_start
            overlay_height = overlay_img_cropped.height

        # Paste the overlay image onto the background image
        bg_img.paste(overlay_img_cropped, (x, y), overlay_img_cropped)

        # Save the result
        bg_img_name = str(i) + ".jpg"
        bg_img.save(os.path.join(save_img_path, bg_img_name))
        
        # Save the bounding box information in YOLO format
        bb_txt_name = str(i) + ".txt"
        with open(os.path.join(save_img_path, bb_txt_name), "w") as f:
            f.write("0 " + str(x/bg_width) + " " + str(y/bg_height) + " " + str(overlay_width/bg_width) + " " + str(overlay_height/bg_height))






def browse_files(entry, select_folder=False):
    if select_folder:
        # Code to open a file browser and get the selected folder path
        folderpath = filedialog.askdirectory()
    else:
        # Code to open a file browser and get the selected file path
        filepath = filedialog.askopenfilename()
        
    # Update the value of the StringVar with the selected path
    entry.delete(0, 'end')
    entry.insert(0, filepath if not select_folder else folderpath)

def generate_images(bg_img_path_entry, overlay_img_path_entry, save_img_path_entry, num_repeats_entry):
    bg_img_path = bg_img_path_entry.get()
    overlay_img_path = overlay_img_path_entry.get()
    save_img_path = save_img_path_entry.get()
    num_repeats = int(num_repeats_entry.get())
    
    bg_img = Image.open(bg_img_path)
    overlay_img = Image.open(overlay_img_path)
    bg_width, bg_height = bg_img.size
    overlay_width, overlay_height = overlay_img.size
    
    #if overlay_width > bg_width or overlay_height > bg_height:
        #response = messagebox.askyesno("Overlay Image size", "The overlay image is larger than the background image on both axis's, would you like to scale the overlay image down to a smaller size?")
        #if response == True:
            ## Scale the overlay image to a smaller size
         #   overlay_img = overlay_img.resize((int(bg_width * 0.2), int(bg_height * 0.2)))
          #  overlay_width, overlay_height = overlay_img.size
        #else:
            #return
    overlay_image_with_bb_cropped(bg_img_path, overlay_img_path, save_img_path, num_repeats)

def upload_parameters():
    # Create a GUI window
    root = tk.Tk()
    root.title("Upload Parameters")

    # Create a label for the background image path
    bg_img_path_label = tk.Label(root, text="Background Image Path:")
    bg_img_path_label.grid(row=0, column=0, padx=10, pady=10)

    # Create a label for the overlay image path
    overlay_img_path_label = tk.Label(root, text="Overlay Image Path:")
    overlay_img_path_label.grid(row=1, column=0, padx=10, pady=10)

    # Create a label for the save image path
    save_img_path_label = tk.Label(root, text="Save Image Path:")
    save_img_path_label.grid(row=2, column=0, padx=10, pady=10)

    # Create a label for the number of repeats
    num_repeats_label = tk.Label(root, text="Number of Repeats:")
    num_repeats_label.grid(row=3, column=0, padx=10, pady=10)

    # Create a text entry for the background image path
    bg_img_path_entry = tk.Entry(root)
    bg_img_path_entry.grid(row=0, column=1, padx=10, pady=10)

    # Create a text entry for the overlay image path
    overlay_img_path_entry = tk.Entry(root)
    overlay_img_path_entry.grid(row=1, column=1, padx=10, pady=10)

    # Create a text entry for the save image path
    save_img_path_entry = tk.Entry(root)
    save_img_path_entry.grid(row=2, column=1, padx=10, pady=10)

    # Create a text entry for the number of repeats
    num_repeats_entry = tk.Entry(root)
    num_repeats_entry.grid(row=3, column=1, padx=10, pady=10)

    # Create a button to browse for background image path
    bg_img_browse_button = tk.Button(root, text="Browse", command=lambda: browse_files(bg_img_path_entry))
    bg_img_browse_button.grid(row=0, column=2, padx=10, pady=10)

    # Create a button to browse for overlay image path
    overlay_img_browse_button = tk.Button(root, text="Browse", command=lambda: browse_files(overlay_img_path_entry))
    overlay_img_browse_button.grid(row=1, column=2, padx=10, pady=10)

    # Create a button to browse for save final image path
    save_img_browse_button = tk.Button(root, text="Browse", command=lambda: browse_files(save_img_path_entry, True))
    save_img_browse_button.grid(row=2, column=2, padx=10, pady=10)

    # Create a button to generate the images and bounding boxs
    generate_button = tk.Button(root, text="Generate", command=lambda: generate_images(bg_img_path_entry, overlay_img_path_entry, save_img_path_entry, num_repeats_entry))
    generate_button.grid(row=4, column=1, padx=10, pady=10)
    
upload_parameters()











    
