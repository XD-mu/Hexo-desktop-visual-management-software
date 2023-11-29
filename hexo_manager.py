import tkinter as tk
from tkinter import simpledialog
import subprocess
import threading
import os
import re

class HexoManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Hexo Blog Manager")
        self.hexo_process = None
        self.create_widgets()

    def create_widgets(self):
        # Button and Input Area
        top_frame = tk.Frame(self.root)
        top_frame.pack(padx=10, pady=5, fill=tk.X)

        # Create Article Button
        self.create_button = tk.Button(top_frame, text="创建新文章", command=self.create_article, bg="#ADD8E6")
        self.create_button.pack(side=tk.LEFT, padx=5)

        # Article Name Entry with placeholder
        self.article_name_entry = tk.Entry(top_frame, width=20)
        self.article_name_entry.insert(0, "请输入文章标题")
        self.article_name_entry.bind("<FocusIn>", self.on_entry_click)
        self.article_name_entry.pack(side=tk.LEFT, padx=5)

        # Generate Article Button
        self.generate_button = tk.Button(top_frame, text="文章生成", command=lambda: self.run_command("hexo g"), bg="#ADD8E6")
        self.generate_button.pack(side=tk.LEFT, padx=5)

        # Serve Article Button
        self.serve_button = tk.Button(top_frame, text="文章预览", command=self.serve_articles, bg="#ADD8E6")
        self.serve_button.pack(side=tk.LEFT, padx=5)

        # Stop Serve Button
        self.stop_serve_button = tk.Button(top_frame, text="终止预览", command=self.stop_serve, bg="#ADD8E6")
        self.stop_serve_button.pack(side=tk.LEFT, padx=5)

        # Deploy Article Button
        self.deploy_button = tk.Button(top_frame, text="文章上传", command=lambda: self.run_command("hexo d"), bg="#ADD8E6")
        self.deploy_button.pack(side=tk.LEFT, padx=5)

        # Clean Button
        self.clean_button = tk.Button(top_frame, text="本地备份清理", command=lambda: self.run_command("hexo clean"), bg="#ADD8E6")
        self.clean_button.pack(side=tk.LEFT, padx=5)

        # Output Text Box
        self.output_text = tk.Text(self.root, height=10, width=50, bg="#000000", fg="#FFFFFF")
        self.output_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def on_entry_click(self, event):
        """Clear the entry on focus."""
        if self.article_name_entry.get() == "请输入文章标题":
            self.article_name_entry.delete(0, tk.END)

    def create_article(self):
        article_name = self.article_name_entry.get()
        if article_name and article_name != "请输入文章标题":
            self.run_command(f"hexo new post \"{article_name}\"")
            typora_path = "D:/Typora/Typora.exe" #修改为你的电脑博客本地Markdown编辑器路径
            file_path = f"E:/HexoLearningCode/source/_posts/{article_name}.md" #修改为你的电脑博客本地Hexo文件夹路径
            subprocess.Popen([typora_path, file_path])
            self.article_name_entry.delete(0, tk.END)


    def run_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd="E:/HexoLearningCode")#注意修改为你的电脑博客本地Hexo文件夹路径
        output, error = process.communicate()
        self.output_text.insert(tk.END, output.decode('utf-8') + error.decode('utf-8'))
        self.output_text.insert(tk.END, f"{command} FUNCTION FINISHED!\n")
        self.scroll_to_end()

    def serve_articles(self):
        # 以线程方式运行，避免阻塞GUI
        self.serve_thread = threading.Thread(target=self.run_command, args=("hexo s",), daemon=True)
        self.serve_thread.start()
        self.output_text.insert(tk.END, "Serve Article FUNCTION FINISHED!\n")
        self.scroll_to_end()

    def stop_serve(self):
        if self.hexo_process:
            self.hexo_process.terminate()
            self.hexo_process = None
        self.output_text.insert(tk.END, "Stop Serve FUNCTION FINISHED!\n")
        self.scroll_to_end()
    def scroll_to_end(self):
        self.output_text.see(tk.END)
if __name__ == "__main__":
    root = tk.Tk()
    app = HexoManager(root)
    root.geometry("800x400")
    root.mainloop()
