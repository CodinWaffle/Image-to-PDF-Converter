import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
from PIL import Image
import os

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, bg="#2B2B2B", fg="white", font=("Helvetica", 12))

        self.initialize_ui()

    def initialize_ui(self):
        title_label = tk.Label(self.root, text="Image to PDF Converter", font=("Helvetica", 16, "bold"), bg="#2B2B2B", fg="white")
        title_label.pack(pady=10)

        select_images_button = tk.Button(self.root, text="Select Images", command=self.select_images, bg="#4B4B4B", fg="white")
        select_images_button.pack(pady=(0, 10))

        self.selected_images_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        label = tk.Label(self.root, text="Enter PDF name: ", bg="#2B2B2B", fg="white")
        label.pack()

        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify='center', bg="#3B3B3B", fg="white")
        pdf_name_entry.pack()

        convert_button = tk.Button(self.root, text="Convert to PDF", command=self.convert_images_to_PDF, bg="#4B4B4B", fg="white")
        convert_button.pack(pady=(20, 40))

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
        self.update_selected_images_listbox()
    
    def update_selected_images_listbox(self):
        self.selected_images_listbox.delete(0, tk.END)

        for image_path in self.image_paths:
            _, image_path = os.path.split(image_path)
            self.selected_images_listbox.insert(tk.END, image_path)
    
    def convert_images_to_PDF(self):
        if not self.image_paths:
            return

        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"
        
        pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))

        for image_path in self.image_paths:
            try:
                img = Image.open(image_path)
                available_width = 540
                available_height = 720
                scale_factor = min(available_width / img.width, available_height / img.height)
                new_width = img.width * scale_factor
                new_height = img.height * scale_factor
                x_centered = (612 - new_width) / 2
                y_centered = (792 - new_height) / 2

                pdf.setFillColor((255, 255, 255))  
                pdf.rect(0, 0, 612, 792, fill=True)
                
               
                pdf.drawImage(image_path, x_centered, y_centered, width=new_width, height=new_height)
                pdf.showPage()
            except Exception as e:
                print(f"Error converting image to PDF: {e}")

        pdf.save()

def main():
    root = tk.Tk()
    root.title("Image to PDF Converter")
    converter = ImageToPDFConverter(root)
    root.geometry("400x600")
    root.configure(bg="#2B2B2B")
    root.mainloop()

if __name__ == "__main__":
    main()