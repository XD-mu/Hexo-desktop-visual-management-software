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
        # 设置窗口图标
        self.root.iconbitmap(r'E:/HexoLearningCode/favicon.ico')
        
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
        
        # 已有文章查看按钮
        self.view_articles_button = tk.Button(top_frame, text="已有文章查看", command=self.toggle_article_list, bg="#ADD8E6")
        self.view_articles_button.pack(side=tk.LEFT, padx=5)

        # 创建一个下拉列表以显示文章列表，并设置样式
        self.article_dropdown = tk.Listbox(self.root, height=10, width=50, bg="#F0F0F0", fg="#000000", font=('Arial', 10))
        articles_dir = "E:/HexoLearningCode/source/_posts"
        md_files = [f[:-3] for f in os.listdir(articles_dir) if f.endswith('.md')]
        for file in md_files:
            self.article_dropdown.insert(tk.END, file)
        self.article_dropdown.bind('<<ListboxSelect>>', self.open_selected_article)
        
    def toggle_article_list(self):
        if hasattr(self, 'article_dropdown') and self.article_dropdown.winfo_viewable():
            self.article_dropdown.place_forget()  # 隐藏下拉列表
        else:
            # 显示下拉列表并设置合适的位置和大小
            x_position = self.view_articles_button.winfo_x() + self.view_articles_button.winfo_width() + 10  # 在按钮右侧留出一些空间
            y_position = self.view_articles_button.winfo_y()
            self.article_dropdown.place(x=x_position, y=y_position, width=200, height=200)

    def open_selected_article(self, event):
        selection = event.widget.curselection()
        if selection:
            selected_article = event.widget.get(selection[0])
            typora_path = "D:/Typora/Typora.exe"  # 保持与之前的路径一致
            file_path = f"E:/HexoLearningCode/source/_posts/{selected_article}.md"
            subprocess.Popen([typora_path, file_path])
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
            self.refresh_article_list()  # 调用刷新文章列表的函数
            
    def refresh_article_list(self):
        if hasattr(self, 'article_dropdown'):
            self.article_dropdown.delete(0, tk.END)  # 清空列表
            articles_dir = "E:/HexoLearningCode/source/_posts"
            md_files = [f[:-3] for f in os.listdir(articles_dir) if f.endswith('.md')]
            for file in md_files:
                self.article_dropdown.insert(tk.END, file)
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
        try:
            # 执行taskkill命令以结束所有node.exe进程
            subprocess.run("taskkill /f /t /im node.exe", check=True, shell=True)
            self.output_text.insert(tk.END, "Node.js server on port 4000 has been stopped.\n")
        except subprocess.CalledProcessError as e:
            self.output_text.insert(tk.END, f"Error stopping Node.js server: {e}\n")
        self.scroll_to_end()

    def scroll_to_end(self):
        self.output_text.see(tk.END)
if __name__ == "__main__":
    root = tk.Tk()
    app = HexoManager(root)
    root.geometry("950x400")
    root.mainloop()
