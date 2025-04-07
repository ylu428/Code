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
    try:
        wafer_size = int(wafer_entry.get().strip())

    except ValueError:
        messagebox.showwarning("Invalid input", "Wafer sizemust be integers.")
        return None
    try:
        num_measurements = int(measure_entry.get().strip())
    except ValueError:
        messagebox.showwarning("Invalid input", "Number of measurements must be an integer.")
        return None


    lot_id = lotid_entry.get().strip()
    return filename, wafer_size, num_measurements, lot_id, True

def prepare_output(df, lot_id, filename1, filename2, wafer_size, num_measurements):
    # Remove extensions from filenames
    name1 = os.path.splitext(os.path.basename(filename1))[0]
    name2 = os.path.splitext(os.path.basename(filename2))[0]

    # Define custom header
    header = ["X", "Y", name1, name2]
    # Create the three special rows (as one-column DataFrames)
    top_rows = pd.DataFrame([
        [f"Wafer Size: {wafer_size} mm"],
        [f"Number of Measurements: {num_measurements}"],
        [f"Lot ID: {lot_id}" if lot_id else "Lot ID: (not specified)"]
    ])

    # Create header row and two empty rows with appropriate width
    header_df = pd.DataFrame([header], columns=df.columns)
    empty_rows = pd.DataFrame([[""] * df.shape[1]] * 2, columns=df.columns)

    # Final output
    bottom_df = pd.concat([header_df, empty_rows, df], ignore_index=True)

    # Combine top and bottom
    result = pd.concat([top_rows, bottom_df], ignore_index=True)

    return result

def save_same_location():
    path1 = file_selector1.get_path()
    path2 = file_selector2.get_path()

    if not (path1 and path2):
        messagebox.showwarning("Missing file", "Please select both files.")
        return

    filename, wafer_size, num_measurements, lot_id, valid = get_inputs()
    if not valid:
        return

    result = extract_columns(path1, path2, max_rows=num_measurements)
    if result is not None:
        final_output = prepare_output(result, lot_id, path1, path2, wafer_size, num_measurements)
        new_path = os.path.join(os.path.dirname(path1), f"{filename}.waf")
        final_output.to_csv(new_path, index=False, header=False)
        messagebox.showinfo("Success", f"File saved to:\n{new_path}")

def save_to():
    path1 = file_selector1.get_path()
    path2 = file_selector2.get_path()

    if not (path1 and path2):
        messagebox.showwarning("Missing file", "Please select both files.")
        return

    filename, wafer_size, num_measurements, lot_id, valid = get_inputs()
    if not valid:
        return

    result = extract_columns(path1, path2, max_rows=num_measurements)
    if result is not None:
        final_output = prepare_output(result, lot_id, path1, path2, wafer_size, num_measurements)
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

# Wafer Size entry
wafer_frame = tk.Frame(app)
tk.Label(wafer_frame, text="Wafer Size (mm):").pack(side=tk.LEFT)
wafer_entry = tk.Entry(wafer_frame, width=10)
wafer_entry.insert(0, "300")
wafer_entry.pack(side=tk.LEFT, padx=5)
wafer_frame.pack(pady=5)

# Combined entry for Number of Measurements
measure_frame = tk.Frame(app)
tk.Label(measure_frame, text="Number of Measurements:").pack(side=tk.LEFT)
measure_entry = tk.Entry(measure_frame, width=10)
measure_entry.insert(0, "49")  # default value
measure_entry.pack(side=tk.LEFT, padx=5)
measure_frame.pack(pady=5)

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
