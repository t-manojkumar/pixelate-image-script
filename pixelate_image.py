import os
from tkinter import filedialog, Tk
from PIL import Image, ImageOps

def pixelate_and_reduce_colors(input_path, output_path, pixel_size=16, color_count=16, dither=False):
    # Open the image
    img = Image.open(input_path)

    # Resize the image to a smaller version (for pixelation)
    small_img = img.resize(
        (img.width // pixel_size, img.height // pixel_size),
        Image.NEAREST
    )

    # Scale it back to the original size
    pixelated_img = small_img.resize(
        (img.width, img.height),
        Image.NEAREST
    )

    # Reduce color palette
    if color_count <= 4:  # For 1-bit and 2-bit, apply dithering if enabled
        reduced_color_img = pixelated_img.convert(
            "1" if color_count == 2 else "P",
            dither=Image.FLOYDSTEINBERG if dither else Image.NONE,
            colors=color_count if color_count > 2 else None
        )
    else:
        reduced_color_img = pixelated_img.convert("P", palette=Image.ADAPTIVE, colors=color_count)

    # Convert to 'RGB' mode if saving as JPEG
    if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
        reduced_color_img = reduced_color_img.convert("RGB")

    # Save the final image
    reduced_color_img.save(output_path)
    print(f"Pixel art image saved as {output_path}")

def select_input_files():
    # Allow user to select single or multiple image files
    root = Tk()
    root.withdraw()  # Hide the main window
    file_paths = filedialog.askopenfilenames(title="Select Image(s)", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    return file_paths

def select_output_folder():
    # Allow user to select the output folder
    root = Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory(title="Select Output Folder")
    return folder_path

def main():
    # Prompt user to choose a bit style
    print("Choose bit style:")
    print("1. 1-bit (2 colors)")
    print("2. 2-bit (4 colors)")
    print("3. 4-bit (16 colors)")
    print("4. 8-bit (256 colors)")
    print("5. 16-bit (65536 colors)")
    print("6. 32-bit (True color, 16777216 colors)")
    choice = int(input("Enter the number corresponding to your choice: "))

    # Map choices to color counts
    bit_styles = {
        1: 2,       # 1-bit
        2: 4,       # 2-bit
        3: 16,      # 4-bit
        4: 256,     # 8-bit
        5: 65536,   # 16-bit
        6: 16777216 # 32-bit (True color)
    }

    color_count = bit_styles.get(choice, 16)  # Default to 4-bit if invalid choice

    # Ask user to enable dithering for 1-bit or 2-bit
    dither = False
    if color_count <= 4:
        dither_input = input("Enable dithering for better gradients? (y/n): ").lower()
        dither = dither_input == 'y'

    # Ask user to select input images
    input_files = select_input_files()
    if not input_files:
        print("No images selected. Exiting...")
        return

    # Ask user for output folder
    output_folder = select_output_folder()
    if not output_folder:
        print("No output folder selected. Exiting...")
        return

    # Process each selected image
    for input_image_path in input_files:
        # Set output image path
        file_name = os.path.basename(input_image_path)
        output_image_path = os.path.join(output_folder, f"pixel_art_{file_name}")

        # Pixelate and reduce color
        pixelate_and_reduce_colors(
            input_image_path, output_image_path, pixel_size=10, color_count=color_count, dither=dither
        )

if __name__ == "__main__":
    main()
