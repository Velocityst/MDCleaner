import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import exifread
import os

class MetaDataCleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MDCleaner")
        self.geometry("500x650")
        self.resizable(False, False)
        self.configure(bg='lightgray')

        self.open_button = ctk.CTkButton(self, text="Open File", command=self.open_file)
        self.open_button.pack(pady=20)

        self.preview_label = ctk.CTkLabel(self, text="MD")
        self.preview_label.pack(pady=10)

        self.metadata_text = ctk.CTkTextbox(self, height=320, width=300)
        self.metadata_text.pack(pady=10)

        self.clean_button = ctk.CTkButton(self, text="Clear", command=self.clean_metadata, state=ctk.DISABLED)
        self.clean_button.pack(pady=10)

        self.file_path = None

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a file", filetypes=[("All Files", "*.*")]
        )
        if not file_path:
            messagebox.showwarning("Error", "You should select a file!")
            return
        self.file_path = file_path
        self.show_preview()
        self.extract_metadata(file_path)
        self.clean_button.configure(state=ctk.NORMAL)

    def show_preview(self):
        img = Image.open(self.file_path)
        img.thumbnail((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        self.preview_label.configure(image=img_tk)
        self.preview_label.image = img_tk

    def extract_metadata(self, file_path):
        try:
            with open(file_path, 'rb') as img_file:
                exif_data = exifread.process_file(img_file)
            self.metadata_text.delete(1.0, ctk.END)
            if exif_data:
                for tag, value in exif_data.items():
                    self.metadata_text.insert(ctk.END, f"{tag}: {value}\n")
            else:
                self.metadata_text.insert(ctk.END, "Can't find any metadata.")
        except Exception as e:
            messagebox.showerror("Error", f"Metadata could not be cleaned: {str(e)}")

    def clean_metadata(self):
        if not self.file_path:
            messagebox.showwarning("Error", "You should select a file!")
            return
        try:
            img = Image.open(self.file_path)
            img_no_exif = img.copy()
            img_no_exif.info.clear()
            directory = os.path.dirname(self.file_path)
            clean_file_name = os.path.join(directory, "cleaned_" + os.path.basename(self.file_path))
            img_no_exif.save(clean_file_name)
            messagebox.showinfo("Successful", f"Metadata has been cleaned and the new file has been saved: {clean_file_name}")

        except Exception as e:
            messagebox.showerror("Error", f"Metadata could not be cleaned: {str(e)}")

if __name__ == "__main__":
    app = MetaDataCleanerApp()
    app.mainloop()
