import os
import tkinter as tk
from tkinter import filedialog, messagebox

def convert_to_little_endian_hex(value):
    return value.to_bytes(4, byteorder='little').hex()

def convert_to_ascii_hex(value):
    return ''.join([f"{ord(c):02x}" for c in str(value)])

def search_and_replace_in_file(file_path, original_value_hex, new_value_hex, output_text):
    with open(file_path, 'rb') as file:
        file_content = file.read()
    
    search_pattern = bytes.fromhex(original_value_hex)
    index = file_content.find(search_pattern)
    
    if index != -1:
        new_file_content = file_content[:index] + bytes.fromhex(new_value_hex) + file_content[index+len(search_pattern):]
        with open(file_path, 'wb') as file:
            file.write(new_file_content)
        output_text.insert(tk.END, "Little-endian patch applied successfully.\n")
    else:
        output_text.insert(tk.END, "Little-endian pattern not found.\n")

def replace_specific_sequence(file_path, position, new_value, output_text):
    new_value_ascii_hex = convert_to_ascii_hex(new_value)
    
    with open(file_path, 'r+b') as file:
        file.seek(position)
        file.write(bytes.fromhex(new_value_ascii_hex))
        output_text.insert(tk.END, f"ASCII patch applied succesfully.\n")

def backup_file(file_path, output_text):
    backup_path = file_path + ".bak"
    if not os.path.exists(backup_path):
        with open(file_path, 'rb') as file:
            content = file.read()
        with open(backup_path, 'wb') as backup:
            backup.write(content)
        output_text.insert(tk.END, "Backup created.\n")
    else:
        output_text.insert(tk.END, "Backup already exists.\n")

def gui():
    def open_file_dialog():
        filename = filedialog.askopenfilename(title="Select mb_warband.exe",
                                              filetypes=(("Executable files", "mb_warband.exe"),))
        if filename:
            file_path_entry.delete(0, tk.END)
            file_path_entry.insert(0, filename)

    def patch_button_clicked():
        file_path = file_path_entry.get()
        if not file_path.endswith("mb_warband.exe"):
            messagebox.showerror("Error", "Selected file is not mb_warband.exe. Please select the correct file.")
            return

        try:
            new_limit = int(new_limit_entry.get())
            if new_limit > 999:
                messagebox.showerror("Error", "The new limit cannot exceed 999.")
                return
            backup_file(file_path, output_text)  # Ensure a backup is made before applying changes

            # Apply little-endian hex replacement
            new_limit_hex = convert_to_little_endian_hex(new_limit)
            original_value_hex = '50000000'  # The pattern to replace
            search_and_replace_in_file(file_path, original_value_hex, new_limit_hex, output_text)

            # Apply ASCII replacement
            position = 4314904  # The specific position for the ASCII replacement
            new_value_ascii_hex = convert_to_ascii_hex(new_limit)  # Convert new limit to ASCII hex
            replace_specific_sequence(file_path, position, new_limit, output_text)

            output_text.insert(tk.END, "All patches applied!\n")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for the new limit.")
        

    root = tk.Tk()
    root.title("Warband Corpse Limit Patcher")
    root.geometry("550x200")  # Adjusted window size for new layout
    root.resizable(False, False)
    root.configure(bg='#333333')

    style = {'font': ('Helvetica', 9), 'bg': '#333333', 'fg': '#ffffff'}

    # Create frames
    left_frame = tk.Frame(root, bg='#333333')
    left_frame.pack(side=tk.LEFT, padx=(10, 5), pady=10, fill=tk.Y, expand=False)

    right_frame = tk.Frame(root, bg='#333333')
    right_frame.pack(side=tk.RIGHT, padx=(5, 10), pady=10, fill=tk.BOTH, expand=True)

    # Widgets for left frame
    file_path_label = tk.Label(left_frame, text="Path to mb_warband.exe:", **style)
    file_path_label.pack(pady=(0, 5))

    file_path_entry = tk.Entry(left_frame, width=40, **style)
    file_path_entry.pack(pady=(0, 5))

    browse_button = tk.Button(left_frame, text="Browse...", command=lambda: open_file_dialog(), **style)
    browse_button.pack(pady=(0, 10))

    new_limit_label = tk.Label(left_frame, text="Enter the new corpse limit (max 999):", **style)
    new_limit_label.pack(pady=(0, 5))

    new_limit_entry = tk.Entry(left_frame, width=20, **style)
    new_limit_entry.pack(pady=(0, 5))

    patch_button = tk.Button(left_frame, text="Apply Patch", command=lambda: patch_button_clicked(), **style)
    patch_button.pack(pady=(0, 5))

    # Widgets for right frame
    # Remove 'bg' and 'fg' from style when applying to output_text to avoid conflicts.
    output_text_style = {'font': ('Helvetica', 9), 'bg': '#1e1e1e', 'fg': '#dcdcdc'}
    output_text = tk.Text(right_frame, height=10, width=30, wrap=tk.WORD, bd=0, highlightthickness=0, **output_text_style)
    output_text.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    # Ensure the text widget is in the 'normal' state before attempting to insert text.
    output_text.configure(state='normal')

    author_label = tk.Label(right_frame, text="Made by SlyCrackz", **style)
    author_label.pack(side=tk.BOTTOM, pady=(5, 0))

    root.mainloop()

if __name__ == "__main__":
    gui()
