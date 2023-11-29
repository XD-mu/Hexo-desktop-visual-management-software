# Hexo desktop visual management software
 适用于患有懒病的user，简化了hexo写博客的操作流程，喜欢的可以给个**Star！**谢谢！

## 简单介绍：

### 先说说他的功能：

1. **创建新文章**： 这个功能允许用户快速创建一篇新的 Hexo 博客文章。用户只需在文本框中输入文章的标题，点击“创建新文章”按钮，软件便会自动在 Hexo 博客中添加一篇新文章，并使用 Typora 编辑器打开它进行编辑。
2. **文章生成**： 用户可以使用这个功能来生成静态的博客内容。它执行 `hexo generate` 命令（简写为 `hexo g`），这会构建整个博客，生成静态的 HTML 文件，准备好用于部署。
3. **文章预览**： 此功能提供了一个本地服务器来预览博客的最新更改。它执行 `hexo server` 命令（简写为 `hexo s`），启动一个本地服务器，允许用户在浏览器中查看博客的实时预览。
4. **终止预览**： 当用户完成预览并希望停止本地服务器时，可以使用这个功能。它会终止正在运行的 Hexo 服务器，使本地预览端口关闭。
5. **文章上传**： 用户通过这个功能可以将本地更改上传到远程服务器。它执行 `hexo deploy` 命令（简写为 `hexo d`），这通常会将生成的静态页面推送到配置的 Git 仓库，如 GitHub Pages 或其他托管服务。
6. **本地备份清理**： 这个功能用于清理本地 Hexo 生成的临时文件。执行 `hexo clean` 命令，清除缓存文件和已生成的静态文件，通常用于解决构建问题或在重大更改后进行清理。

![示意图](https://s2.loli.net/2023/11/29/KSFgL5brdhVQ9nu.png)

​	采用了可视化的hexo的博客撰写上传装置，前提是要配好桌面的Git Bash上传和有着本地的Hexo文件夹，以及文本编辑器（我用的是Typora，难道他不香嘛？）。按照我下面提到的步骤运行程序。接下来，你就可以愉快的使用啦！

**下面说说使用方法：**

​	**1.修改代码内对应你自己电脑相应软件的路径**

```python
typora_path = "D:/Typora/Typora.exe" #修改为你的电脑博客本地Markdown编辑器路径
```

```python
file_path = f"E:/HexoLearningCode/source/_posts/{article_name}.md" #修改为你的电脑博客本地Hexo文件夹路径
```

```py
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd="E:/HexoLearningCode")#注意修改为你的电脑博客本地Hexo文件夹路径
```

​	**2.确保你的电脑配好桌面的Git Bash上传和有着本地的Hexo文件夹**

​	**3.确保安装想应的依赖包和pyinstaller**

​	**4.然后在该程序文件同路径运行这段程序找到对应的exe文件就可以愉快的写作啦！**

```python
pyinstaller --onefile --noconsole --clean hexo_manager.py
```

