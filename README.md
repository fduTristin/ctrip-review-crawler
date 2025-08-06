# 携程酒店评论爬取

## 项目简介

本项目用于爬取携程网指定城市的酒店信息及其评论数据，并将结果保存为 JSON 文件。

## 使用方法

1. **克隆项目**

   ```bash
   git clone <项目地址>
   cd xiecheng
   ```

2. **创建虚拟环境**

   使用 Conda 创建虚拟环境：

   ```bash
   conda create -n xiecheng_env python=3.11 -y
   conda activate xiecheng_env
   ```

3. **安装依赖**

   使用 `requirements.txt` 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

4. **运行项目**

   修改 `main.py` 中的配置参数（如 `cityId`、`numHotelPages` 和 `numCommentPages`），然后运行：

   ```bash
   python main.py
   ```

5. **查看结果**

   - 酒店信息保存在 `hotels.json` 文件中。
   - 每个酒店的详细信息和评论保存在 `outputs` 文件夹中。

## 配置说明

### 参数配置

- `cityId`：城市 ID（1: 北京, 2: 上海, 3: 广州, 4: 深圳）。
- `numHotelPages`：爬取的酒店页数。
- `numCommentPages`：爬取的评论页数。

### 输出文件

- `hotels.json`：包含所有酒店的基本信息。
- `outputs/hotel_<hotel_id>.json`：每个酒店的详细信息及评论。

> [!note]
>
> - 确保网络连接正常，且目标网站允许爬取。
> - 线程开太多会被封，正在尝试搞代理池
> - 由于本人技术有限，不确定请求负载能否持久使用，可以自己上网抓包更新一下 `formdata`
