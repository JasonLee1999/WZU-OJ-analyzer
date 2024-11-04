# WZU-OJ-analyzer

## 项目概述

本项目包含两个Python脚本：`get_data.py` 和 `analyse_data.py`，以及一个配置文件 `config.json`。这些文件共同工作，用于从WZU-OJ中获取提交数据，分析这些数据，并最终将分析结果保存到Excel文件中。

## 配置文件 `config.json`

配置文件 `config.json` 包含必要的配置信息，如Cookie和URL。请确保该文件中的Cookie和URL是最新的，并且URL是可访问的。如果遇到网络问题，可能需要检查URL的合法性或稍后重试。

```json
{
    "Cookie": "csrftoken=********************************; sessionid=********************************",
    "url": "http://10.132.246.246/judge/course/1/judgelist/?num=50"
}
```

### 如何获取 URL

获取URL的过程实际上就是访问特定网页并复制该网页地址的过程。以下是详细步骤，用于获取你想要分析的课程的状态页面的URL：

1. **访问课程页面**：在浏览器中输入WZU-OJ的网址，并导航到你想要分析的课程页面。

2. **进入状态页面**：在课程页面中导航到状态页面。

3. **复制URL**：一旦你进入了状态页面，查看浏览器地址栏中的网址。这就是你需要的URL（例如：`http://10.132.246.246/judge/course/1/judgelist/?num=50`）。右键点击地址栏，然后选择“复制”或者使用快捷键（通常是`Ctrl+C`或`Cmd+C`）来复制URL。

4. **粘贴URL**：将复制的URL粘贴到 `config.json` 文件中的 `"url"` 字段。

### 如何获取 Cookie

Cookie 是一种由服务器发送到用户浏览器并保存在本地的小型文本文件，用于识别用户会话。在本项目中，Cookie 用于验证用户身份并获取数据。以下是获取 Cookie 的步骤：

1. **访问目标网站**：在浏览器中打开目标网站（例如：`http://10.132.246.246/judge/course/1/judgelist/?num=50`或`https://10-132-246-246.webvpn.wzu.edu.cn/judge/course/1/judgelist/?num=50`），并确保你已经登录。

2. **检查网络请求**：使用浏览器的开发者工具（通常可以通过按 F12 或右键点击页面元素选择“检查”来打开）。

3. **查看请求头**：在开发者工具的“网络”（Network）标签页中，刷新页面以捕获网络请求。找到对应于目标网站的请求（一般为：`/judgelist/?num=50`），并查看其请求头（Headers）。

4. **复制 Cookie**：在请求头中找到 `Cookie` 字段，并复制其值。确保复制的 Cookie 包含所有必要的会话信息。（例如：`csrftoken=*; sessionid=*`或`csrftoken=*; sessionid=*; _webvpn_key=*.*; webvpn_username=*`）

5. **更新配置文件**：将复制的 Cookie 值粘贴到 `config.json` 文件中的 `"Cookie"` 字段。

请注意，Cookie 通常包含敏感信息，因此请确保在安全的环境中处理，并避免在公共或不安全的地方泄露 Cookie 值。

如果你在获取 Cookie 时遇到问题，可能需要检查你的网络连接，或者确认你是否有足够的权限访问目标网站。如果问题持续存在，可能需要联系网站的技术支持以获取帮助。

## `get_data.py` 脚本

该脚本负责从配置文件中指定的URL获取数据，并将其保存到Excel文件中。它首先读取配置文件，然后使用提供的Cookie发送HTTP请求。获取到的提交数据将被解析并存储在列表中，最后转换为Pandas DataFrame并保存到Excel文件。

## `analyse_data.py` 脚本

该脚本用于分析由 `get_data.py` 脚本获取的数据。它定义了 `Submission`、`User` 和 `Problem` 类来组织数据，并计算问题的难度和用户的排名分。分析结果将被保存到两个Excel文件中：`problems_data.xlsx` 和 `sorted_users.xlsx`。

## 使用说明

1. 确保 `config.json` 文件中的Cookie和URL是最新的。
2. 确保安装了所有必要的Python库，包括 `requests`、`bs4` 和 `pandas`。
3. 运行 `get_data.py` 脚本以从指定URL获取数据并保存到Excel文件。
4. 运行 `analyse_data.py` 脚本以分析数据并生成分析结果。

## 依赖库

- `requests`：用于发送HTTP请求。
- `beautifulsoup4`（bs4）：用于解析HTML。
- `pandas`：用于数据处理和Excel文件操作。

## 运行环境

- Python 3.12.6
- 确保所有依赖库已安装。

通过遵循上述步骤，您可以成功运行本项目，获取和分析数据。如果有任何问题，请检查依赖库的版本，并确保网络连接正常。
