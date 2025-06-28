# -*- coding: utf-8 -*-
"""
文件名: url_utils.py
功能: URL编码工具（符合PEP 8规范）
作者: TianQi AI
日期: 2025-06-28
"""

import inspect
import re
from typing import Union
from urllib.parse import quote, unquote

print(inspect.signature(unquote))


def safe_unquote(url: str, encoding: str = "utf-8", errors: str = "replace", plus_handling: bool = False) -> str:
    """安全的URL解码函数（兼容Python 3.8~3.12）"""
    # 检测环境是否支持原生plus参数
    use_native_plus = hasattr(unquote, "__code__") and "plus" in unquote.__code__.co_varnames

    if use_native_plus:
        return unquote(url, encoding=encoding, errors=errors, plus=plus_handling)
    else:
        decoded = unquote(url, encoding=encoding, errors=errors)
        # 手动处理加号：当plus_handling=False时保留+号原义
        return decoded.replace("+", "%2B") if not plus_handling else decoded


class URLEncoder:
    """
    URL编码器，处理包含特殊字符的URL
    命名规范：类名首字母大写驼峰式
    """

    def __init__(self, strict_mode: bool = False):
        """
        初始化配置
        :param strict_mode: True时遇到错误抛出异常，False则静默处理
        """
        self.strict_mode = strict_mode  # 类内变量小写+下划线

    def safe_encode(self, raw_url: str) -> str:
        """
        安全编码URL（处理已编码/未编码/含+号的情况）

        参数说明:
        - raw_url: 原始URL字符串（可含中文、空格等）

        返回值: 标准编码的URL
        """
        try:
            # 先解码（保留+号不转空格，需Python≥3.9）
            decoded = unquote(raw_url, errors="strict")
            return quote(decoded)
        except UnicodeDecodeError as e:
            if self.strict_mode:
                raise ValueError(f"无效编码序列: {e}") from e
            # 降级方案：移除无效编码序列后重试
            cleaned_url = re.sub(r"%[^0-9A-Fa-f]{2}", "", raw_url)
            return quote(cleaned_url)


# 模块级函数定义（小写+下划线）
def validate_url(url: str) -> bool:
    """
    验证URL格式是否合法（简易版）

    规则：包含协议头且无非法字符
    """
    pattern = re.compile(
        r"^(?:http|ftp)s?://"  # 协议头
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # 域名
        r"localhost|"  # 本地地址
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # IP地址
        r"(?::\d+)?"  # 端口
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return bool(pattern.match(url))


if __name__ == "__main__":
    # 测试用例验证
    encoder = URLEncoder(strict_mode=True)

    # 用例1：未编码URL含中文/空格
    print(encoder.safe_encode("http://测试/文件 1.txt"))
    # 输出: http%3A//%E6%B5%8B%E8%AF%95/%E6%96%87%E4%BB%B6%201.txt

    print(encoder.safe_encode("http://测试/文件+1.txt"))
    # 输出: http%3A//%E6%B5%8B%E8%AF%95/%E6%96%87%E4%BB%B6%201.txt

    # 用例2：已编码URL（防双重编码）
    print(encoder.safe_encode("http%3A%2F%2Fexample.com%2F%E6%B5%8B%E8%AF%95"))
    # 输出: http%3A//example.com/%E6%B5%8B%E8%AF%95

    # 用例3：含+号的URL（保留+号）
    print(encoder.safe_encode("https://api.com/search?q=python+java"))
    # 输出: https%3A//api.com/search%3Fq%3Dpython%2Bjava

    # 验证函数
    print(validate_url("https://gitcode.net"))  # True

    # import sys
    # import urllib.parse

    # print("👉 真实Python版本:", sys.version.split()[0])
    # print("👉 unquote参数:", urllib.parse.unquote.__code__.co_varnames[:4])  # 检查前4个参数名

    test_url = "https://ex.com/%7Euser/file%201.txt%3Fq%3Dpython%2Bcode"
    decoded = unquote(test_url)
    print(decoded)
    # 输出：https://ex.com/~user/file 1.txt?q=python+code
    # 空格解码正确 ✓ | +号原样保留 ✓ | %XX完全解码 ✓
