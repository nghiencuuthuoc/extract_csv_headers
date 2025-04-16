import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def find_csv_files(folder_path):
    csv_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".csv"):
                csv_files.append(os.path.join(root, file))
    return csv_files

def extract_and_save_headers(input_folder, output_folder):
    csv_files = find_csv_files(input_folder)
    if not csv_files:
        messagebox.showwarning("No CSV", "Không tìm thấy file CSV nào trong thư mục.")
        return

    for file_path in csv_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)

            filename = os.path.splitext(os.path.basename(file_path))[0]
            output_file = os.path.join(output_folder, f"{filename}_header.csv")
            with open(output_file, 'w', encoding='utf-8', newline='') as out_f:
                writer = csv.writer(out_f)
                writer.writerow(header)
        except Exception as e:
            print(f"Lỗi khi xử lý {file_path}: {e}")

    messagebox.showinfo("Hoàn tất", f"Đã trích xuất header từ {len(csv_files)} file!")

# Giao diện người dùng
def run_gui():
    def browse_input():
        folder = filedialog.askdirectory()
        if folder:
            input_var.set(folder)

    def browse_output():
        folder = filedialog.askdirectory()
        if folder:
            output_var.set(folder)

    def start_extraction():
        input_folder = input_var.get()
        output_folder = output_var.get()
        if not os.path.isdir(input_folder) or not os.path.isdir(output_folder):
            messagebox.showerror("Lỗi", "Vui lòng chọn cả thư mục Input và Output hợp lệ.")
            return
        extract_and_save_headers(input_folder, output_folder)

    root = tk.Tk()
    root.title("🗂️ Trích xuất Header CSV")

    ttk.Label(root, text="Thư mục chứa file CSV (input):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    input_var = tk.StringVar()
    ttk.Entry(root, textvariable=input_var, width=50).grid(row=0, column=1, padx=5)
    ttk.Button(root, text="Chọn...", command=browse_input).grid(row=0, column=2, padx=5)

    ttk.Label(root, text="Thư mục lưu header (output):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    output_var = tk.StringVar()
    ttk.Entry(root, textvariable=output_var, width=50).grid(row=1, column=1, padx=5)
    ttk.Button(root, text="Chọn...", command=browse_output).grid(row=1, column=2, padx=5)

    ttk.Button(root, text="🚀 Bắt đầu trích xuất", command=start_extraction).grid(row=2, column=1, pady=15)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
