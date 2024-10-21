# GitHub 存储库管理器

此脚本允许你通过获取所有的 GitHub 存储库并选择性地删除它们来管理你的 GitHub 存储库。

## 先决条件

- Python 3.6 或更高版本
- pip（Python 包安装程序）

## 设置

1. 克隆此存储库或下载文件。

2. 安装所需的软件包：

   ```
   pip install -r requirements.txt
   ```

3. 在与脚本相同的目录中创建一个`.env`文件，内容如下：

   ```
   GITHUB_TOKEN=你的 GitHub 令牌在这里
   GITHUB_USERNAME=你的 GitHub 用户名在这里
   ```

   将“你的 GitHub 令牌在这里”替换为你的 GitHub 个人访问令牌，将“你的 GitHub 用户名在这里”替换为你的 GitHub 用户名。

## 使用方法

使用以下命令运行脚本：

```
python main.py
```

按照提示选择并删除存储库。

## 警告

删除存储库是不可逆转的。请谨慎使用此脚本。
