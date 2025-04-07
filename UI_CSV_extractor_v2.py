import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class FileSelector:
    def __init__(self, master, label_text):
        self.file_path = None

        self.frame = tk.Frame(master)
        self.label = tk.Label(self.frame, text=label_text + ": Not selected", wraplength=400)
        self.label.pack(side=tk.LEFT, padx=5)

        self.button = tk.Button(self.frame, text=f"Select {label_text}", command=self.select_file)
        self.button.pack(side=tk.RIGHT)

        self.frame.pack(pady=5, fill="x")

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if path:
            self.file_path = path
            self.label.config(text=f"{self.button['text']}: {path}")

    def get_path(self):
        return self.file_path

def extract_columns(file1, file2, max_rows=None):
    try:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        cols1 = df1.iloc[:, [5, 6, 22]]  # File 1: columns 6, 7, 23
        col2 = df2.iloc[:, [22]]        # File 2: column 23

        combined = pd.concat([cols1, col2], axis=1)

        if max_rows is not None:
            combined = combined.head(max_rows)

        return combined
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def get_inputs():
    filename = filename_entry.get().strip()
    if not filename:
        filename = "combined"

    length_text = length_entry.get().strip()
    if length_text:
        try:
            length = int(length_text)
            if length <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Length", "Please enter a valid positive integer.")
            return filename, None, None, False
    else:
        length = None

    lot_id = lotid_entry.get().strip()
    return filename, length, lot_id, True

def prepare_output(df, lot_id, filename1, filename2):
    # Remove extensions from filenames
    name1 = os.path.splitext(os.path.basename(filename1))[0]
    name2 = os.path.splitext(os.path.basename(filename2))[0]

    # Define custom header
    header = ["X", "Y", name1, name2]
    # Create empty rows for shifting
    empty_rows = pd.DataFrame([[""] * df.shape[1]] * 2, columns=df.columns)

    # Build the final DataFrame with Lot ID and Header
    lot_id_row = [f"Lot ID: {lot_id}" if lot_id else "Lot ID: (not specified)"] + [""] * (df.shape[1] - 1)
    final_df = pd.DataFrame([lot_id_row], columns=df.columns)

    # Add header and actual data
    header_df = pd.DataFrame([header], columns=df.columns)
    result = pd.concat([final_df, empty_rows, header_df, df], ignore_index=True)

    return result

def save_same_location():
    path1 = file_selector1.get_path()
    path2 = file_selector2.get_path()

    if not (path1 and path2):
        messagebox.showwarning("Missing file", "Please select both files.")
        return

    filename, length, lot_id, valid = get_inputs()
    if not valid:
        return

    result = extract_columns(path1, path2, max_rows=length)
    if result is not None:
        final_output = prepare_output(result, lot_id, path1, path2)
        new_path = os.path.join(os.path.dirname(path1), f"{filename}.waf")
        final_output.to_csv(new_path, index=False, header=False)
        messagebox.showinfo("Success", f"File saved to:\n{new_path}")

def save_to():
    path1 = file_selector1.get_path()
    path2 = file_selector2.get_path()

    if not (path1 and path2):
        messagebox.showwarning("Missing file", "Please select both files.")
        return

    filename, length, lot_id, valid = get_inputs()
    if not valid:
        return

    result = extract_columns(path1, path2, max_rows=length)
    if result is not None:
        final_output = prepare_output(result, lot_id, path1, path2)
        initialfile = f"{filename}.waf"
        save_path = filedialog.asksaveasfilename(defaultextension=".waf",
                                                 filetypes=[("CSV files", "*.waf")],
                                                 initialfile=initialfile)
        if save_path:
            final_output.to_csv(save_path, index=False, header=False)
            messagebox.showinfo("Success", f"File saved to:\n{save_path}")

# GUI setup
app = tk.Tk()
app.title("OCD raw data extractor")

file_selector1 = FileSelector(app, "File 1")
file_selector2 = FileSelector(app, "File 2")

# Output filename entry
filename_frame = tk.Frame(app)
tk.Label(filename_frame, text="Output Filename (no extension):").pack(side=tk.LEFT)
filename_entry = tk.Entry(filename_frame, width=30)
filename_entry.pack(side=tk.LEFT, padx=5)
filename_frame.pack(pady=5)

# Data length entry
length_frame = tk.Frame(app)
tk.Label(length_frame, text="Number of Data Points to Copy:").pack(side=tk.LEFT)
length_entry = tk.Entry(length_frame, width=10)
length_entry.pack(side=tk.LEFT, padx=5)
length_frame.pack(pady=5)

# Lot ID entry
lotid_frame = tk.Frame(app)
tk.Label(lotid_frame, text="Lot ID:").pack(side=tk.LEFT)
lotid_entry = tk.Entry(lotid_frame, width=30)
lotid_entry.pack(side=tk.LEFT, padx=5)
lotid_frame.pack(pady=5)

# Buttons
save_btn = tk.Button(app, text="Save (Same Location as File 1)", command=save_same_location)
save_btn.pack(pady=5)

save_to_btn = tk.Button(app, text="Save To...", command=save_to)
save_to_btn.pack(pady=5)

app.mainloop()
