import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

# 支持的图片格式
SUPPORTED_FORMATS = (".png", ".jpg", ".jpeg",".tif")

# 模拟预测函数
def predict_genotype(image_path):
    return [
        ("Genotype A", "95%"),
        ("Genotype B", "85%"),
        ("Genotype C", "75%"),
        ("Genotype D", "65%"),
        ("Genotype E", "55%"),
        # 这是示例，用实际预测函数代替
    ]

def open_file():
    # 上传单张图片
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.tif")])
    if file_path:
        show_results_window([file_path])  

def open_folder():
    # 上传包含图片的文件夹
    folder_path = filedialog.askdirectory()
    if folder_path:
        # 获取文件夹内的所有图片文件
        image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(SUPPORTED_FORMATS)]
        if image_files:
            show_results_window(image_files)  
        else:
            tk.messagebox.showwarning("No Images Found", "The selected folder does not contain any valid image files.")

def show_results_window(file_paths):
    # 创建结果窗口
    result_window = tk.Toplevel(root)
    result_window.title("Prediction Results")
    result_window.geometry("600x400")
    result_window.config(bg="#ffffff")

    # 当前页索引
    current_index = tk.IntVar(value=0)

    # 表头
    result_label = tk.Label(result_window, text="Predicted Genotypes and Confidence Intervals", 
                            font=("Arial", 12, "bold"), bg="#ffffff", fg="#333")
    result_label.pack(pady=10)

    # 表格
    columns = ("Genotype", "Confidence Interval")
    tree = ttk.Treeview(result_window, columns=columns, show="headings", height=5)
    tree.heading("Genotype", text="Genotype")
    tree.heading("Confidence Interval", text="Confidence Interval")
    tree.column("Genotype", width=250, anchor="center")
    tree.column("Confidence Interval", width=250, anchor="center")
    tree.pack(pady=10)

    # 图片名称标签
    image_label = tk.Label(result_window, text="", font=("Arial", 10, "italic"), bg="#ffffff", fg="#555")
    image_label.pack()

    # 导航按钮
    button_frame = tk.Frame(result_window, bg="#ffffff")
    button_frame.pack(pady=10)

    prev_button = ttk.Button(button_frame, text="Previous", command=lambda: change_page(-1, current_index, file_paths, tree, image_label, prev_button, next_button))
    prev_button.grid(row=0, column=0, padx=10)

    next_button = ttk.Button(button_frame, text="Next", command=lambda: change_page(1, current_index, file_paths, tree, image_label, prev_button, next_button))
    next_button.grid(row=0, column=1, padx=10)

    # 初始化第一页
    update_page(current_index.get(), file_paths, tree, image_label, prev_button, next_button)

    # 关闭按钮
    close_button = ttk.Button(result_window, text="Close", command=result_window.destroy)
    close_button.pack(pady=10)

def update_page(index, file_paths, tree, image_label, prev_button, next_button):
    # 更新页面函数
    # 清空表格
    for row in tree.get_children():
        tree.delete(row)

    # 获取当前图片的预测结果
    file_path = file_paths[index]
    predictions = predict_genotype(file_path)

    # 填充表格
    for genotype, confidence in predictions:
        tree.insert("", "end", values=(genotype, confidence))

    # 更新图片名称显示
    image_label.config(text=f"Image: {os.path.basename(file_path)}")

    # 更新导航按钮状态
    prev_button.config(state="normal" if index > 0 else "disabled")
    next_button.config(state="normal" if index < len(file_paths) - 1 else "disabled")

def change_page(delta, current_index, file_paths, tree, image_label, prev_button, next_button):
    #切换页面函数
    new_index = current_index.get() + delta
    current_index.set(new_index)
    update_page(new_index, file_paths, tree, image_label, prev_button, next_button)

root = tk.Tk()
root.title("Wing Genotype Recognition")
root.geometry("400x300")
root.config(bg="#f0f0f0")  

# 标题
title_label = tk.Label(root, text="Wing Genotype Recognition", 
                       font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=20)

# 上传单张图片按钮
upload_file_button = ttk.Button(root, text="Upload Photo", command=open_file)
upload_file_button.pack(pady=10)

# 上传文件夹按钮
upload_folder_button = ttk.Button(root, text="Upload Folder", command=open_folder)
upload_folder_button.pack(pady=10)

# 底部标识
footer_label = tk.Label(root, text="BIA Group 8", font=("Arial", 10), bg="#f0f0f0", fg="#888")
footer_label.pack(side="bottom", pady=10)

root.mainloop()
