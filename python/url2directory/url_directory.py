# -*- coding=utf-8 -*-
"""
目标:

构建一个用于存储和管理网站结构的数据库系统。该系统需要能够：

存储多个网站的结构: 每个网站可以有多个根节点，并形成树状结构。
建立节点之间的关系: 明确每个节点的父节点，以便表示网站的层次结构。
灵活扩展: 能够适应不同网站的结构，并方便添加新的字段或表。
高效查询: 能够快速查询节点信息、父子关系等。
具体需求:

数据表:
roots: 存储网站的根节点信息，包括 URL 等。
nodes: 存储节点信息，包括标题、父节点 ID 等。
roots_nodes: 建立 roots 和 nodes 之间的关联，明确每个节点属于哪个根节点。
节点关系:
每个节点都有一个唯一的 ID。
每个节点可以有一个父节点，根节点的父节点为 NULL。
roots_nodes 表用于记录节点和对应的根节点之间的关联关系。
数据存储:
存储节点的标题、URL（存储在 roots 表中）、父节点 ID 等信息。
数据查询:
查询某个节点的子节点。
查询某个节点的父节点。
查询某个根节点下的所有节点。
优化点:

性能优化: 对于大型数据集，考虑使用批量插入、索引、分区等技术提高查询效率。
数据一致性: 保证 roots_nodes 表中的数据与 roots 表和 nodes 表保持一致。
灵活扩展: 设计数据库结构时，考虑未来的扩展性，例如添加新的字段或表。
问题与挑战:

节点与根节点的关联: 如何准确地建立节点与根节点之间的关联关系，尤其是当一个节点可以属于多个根节点时。
数据一致性: 如何保证在插入、更新、删除数据时保持数据的一致性。
性能优化: 如何在保证数据完整性的前提下，提高数据库的查询性能。
"""
import sqlite3

from bs4 import BeautifulSoup
from selenium import webdriver


def recursive_crawl(url, selector, parent_id, data):
    """
    递归爬取网页，构建节点数据

    Args:
        url: 当前页面的 URL
        selector: 选择器的 XPath 表达式
        parent_id: 父节点在 nodes 表中的 ID
        data: 存储节点数据的列表
    """

    # 启动浏览器
    driver = webdriver.Chrome()  # 替换为其他浏览器驱动
    driver.get(url)

    # 获取页面源代码
    html_content = driver.page_source

    # 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.select_one(selector)
    for element in elements:
        title = element.text.strip()
        data.append({'title': title, 'parent_id': parent_id})
        recursive_crawl(element.get('href'), selector, len(data) - 1, data)


def save_to_db(start_urls, data, db_conn):
    """
    将爬取的数据保存到数据库

    Args:
        start_urls: 起始 URL 列表
        data: 节点数据列表
        db_conn: 数据库连接
    """

    cursor = db_conn.cursor()

    # 创建表（如果不存在）
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS roots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT
        );
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id INTEGER,
            title TEXT
        );
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS roots_nodes (
            root_id INTEGER,
            node_id INTEGER,
            PRIMARY KEY (root_id, node_id),
            FOREIGN KEY (root_id) REFERENCES roots(id),
            FOREIGN KEY (node_id) REFERENCES nodes(id)
        );
    """
    )

    # 插入根节点
    root_ids = []
    for url in start_urls:
        cursor.execute("INSERT INTO roots (url) VALUES (?)", (url,))
        root_ids.append(cursor.lastrowid)

    # 插入节点
    cursor.executemany(
        "INSERT INTO nodes (parent_id, title) VALUES (?, ?)", [(node['parent_id'], node['title']) for node in data]
    )

    # 插入 roots_nodes 关联表
    # 假设每个节点都属于一个根节点，这里简化处理
    # 实际应用中可能需要更复杂的逻辑
    for i, node in enumerate(data):
        if node['parent_id'] is None:
            # 根节点，直接关联到对应的根节点
            root_id = root_ids[i]
        else:
            # 非根节点，关联到父节点对应的根节点
            # ... (这里需要根据您的具体业务逻辑获取父节点对应的根节点)
            root_id = ...  # 根据您的业务逻辑获取 root_id
        cursor.execute("INSERT INTO roots_nodes (root_id, node_id) VALUES (?, ?)", (root_id, i + 1))

    db_conn.commit()


def main():
    # 示例用法
    # http://192.168.124.80:5344/教育/编程开发
    start_urls = [
        "http://192.168.124.80:5344/%E6%95%99%E8%82%B2/%E7%BC%96%E7%A8%8B%E5%BC%80%E5%8F%91",
        "http://example2.com",
    ]
    selector = ['//*[@id="root"]/div[2]/div/div[1]', "a"]  # 爬取所有链接
    data = []

    dbname = "/tmp/url2dir.db"
    recursive_crawl(start_urls[0], selector[0], None, data)
    # db_conn = sqlite3.connect(dbname)
    # save_to_db(start_urls, data, db_conn)
    # db_conn.close()


if __name__ == "__main__":
    main()
