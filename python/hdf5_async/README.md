# HDF5 Async: 异步 HDF5 客户端/服务器

HDF5 Async 提供了一个高性能、异步的客户端-服务器框架，用于通过网络访问 HDF5 文件。它旨在解决多个进程或机器并发写入单个 HDF5 文件时面临的挑战——这种情况通常会导致文件损坏或需要复杂且缓慢的锁定机制。

本项目非常适合分布式系统，例如数据采集管道、科学计算集群或并行模拟，在这些场景下，多个数据源需要高效、安全地将结果流式传输到中心的 HDF5 文件中。

---

## 目录

- [项目概述](#项目概述)
- [核心功能](#核心功能)
- [系统架构](#系统架构)
- [安装与配置](#安装与配置)
- [如何运行](#如何运行)
- [客户端用法示例](#客户端用法示例)
- [运行测试](#运行测试)
- [贡献](#贡献)

---

## 项目概述

本项目是一个用于 HDF5 文件的异步操作库。它支持多进程和多线程操作，旨在提高 HDF5 文件的读写效率。服务器端提供了数据压缩选项（默认不压缩），并支持多种数据类型的存储和读取。

## 核心功能

- **异步 I/O**: 基于 Python 的 `asyncio` 构建，以最小的开销处理数千个并发客户端连接。
- **安全的并发访问**: 单一服务器管理所有文件 I/O，序列化写操作以防止并发访问导致的数据损坏。
- **非阻塞架构**: 服务器使用 `ThreadPoolExecutor` 来处理阻塞的 HDF5 文件操作，确保主网络事件循环保持响应。
- **高效的序列化**: 使用 **MessagePack** 进行快速、紧凑的二进制序列化，并内置了对复杂 **NumPy 数组**（包括结构化数组）的强大支持。
- **灵活的压缩选项**: 客户端可以为每个独立的 `write`、`update`、`append` 或 `insert` 操作指定压缩算法（例如 `gzip`）。
- **丰富的数据类型支持**: 原生处理 Python 标量（`int`, `float`, `str`）、列表以及多种 NumPy 数组数据类型。
- **全面的 API**: 客户端支持 `create_group`、`read`、`write`、`update`、`delete`、`append` 和 `insert` 操作。
- **智能去重**: 在追加数据时，可选择性地对结构化数组按指定字段（如 `timestamp`）进行去重，确保数据唯一性。

## 系统架构

系统由一个管理 HDF5 文件的中央服务器和多个通过网络连接到它的客户端组成。

- **服务器**: 监听 TCP 连接，使用 `asyncio` 高效管理客户端。它将阻塞的 HDF5 文件操作卸载到工作线程中，以保持主事件循环的响应性。
- **客户端**: 提供一个用户友好的异步 API，封装了所有网络通信细节。`write()`、`read()` 等方法都是 `async` 函数，易于集成。
- **序列化**: 数据使用 **MessagePack** 进行序列化，它比 JSON 更快、更紧凑。通过 `msgpack-numpy` 扩展，可以高效处理 NumPy 数组。

## 安装与配置

### 安装

1.  **克隆仓库**:
    ```bash
    git clone https://github.com/phaos/hdf5_async.git
    cd hdf5_async
    ```

2.  **创建并激活虚拟环境**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **安装依赖**:
    *   **注意**: `h5py` 需要 HDF5 C 库。在 Debian/Ubuntu 上，可以通过 `sudo apt-get install libhdf5-dev` 安装。
    ```bash
    pip install -r requirements.txt
    ```

### 配置 (`config.ini`)

服务器和客户端的行为由 `config.ini` 控制。

```ini
[server]
host = 0.0.0.0
port = 8888
hdf5_file_path = data.h5
use_compression = false
debug = false
serialization_format = messagepack
```

- `host`: 服务器监听的 IP 地址。`0.0.0.0` 表示监听所有网络接口。
- `port`: 服务器监听的端口。
- `hdf5_file_path`: 服务器管理的 HDF5 文件的路径。
- `use_compression`: 是否默认启用压缩（`gzip`）。客户端可以在每次请求中覆盖此设置。
- `debug`: 是否启用详细的调试日志。
- `serialization_format`: 序列化格式，推荐使用 `messagepack`。

## 如何运行

### 启动服务器

在项目根目录运行 `run_server.py` 脚本：

```bash
python run_server.py
```

服务器将根据 `config.ini` 中的设置启动并监听连接。

### 客户端用法示例

以下是一个全面的客户端用法示例，演示了大部分核心功能。

```python
import asyncio
import numpy as np
from client.client import HDF5Client

async def main():
    """主函数，运行所有 HDF5 客户端测试。"""
    client = HDF5Client()
    await client.connect()

    try:
        # 1. 测试基本 CRUD 操作
        print("\n--- 测试基本 CRUD 操作 ---")
        await client.create_group("/my_group")
        data_to_write = np.array([1, 2, 3, 4, 5])
        await client.write("/my_group/my_dataset", data_to_write)
        read_data = await client.read("/my_group/my_dataset")
        assert np.array_equal(data_to_write, read_data)
        print("基本 CRUD 操作验证成功。")

        # 2. 测试不同的数据类型
        print("\n--- 测试不同的数据类型 ---")
        await client.write("/my_group/string_data", "Hello HDF5!")
        read_str = await client.read("/my_group/string_data")
        assert read_str[0] == "Hello HDF5!"
        print("字符串数据验证成功。")

        # 3. 测试追加和插入操作
        print("\n--- 测试追加和插入操作 ---")
        await client.append("/my_group/my_dataset", np.array([6, 7]))
        read_appended = await client.read("/my_group/my_dataset")
        assert np.array_equal(read_appended, [1, 2, 3, 4, 5, 6, 7])
        print("追加操作验证成功。")

        await client.insert("/my_group/my_dataset", 2, np.array([98, 99]))
        read_inserted = await client.read("/my_group/my_dataset")
        assert np.array_equal(read_inserted, [1, 2, 98, 99, 3, 4, 5, 6, 7])
        print("插入操作验证成功。")

        # 4. 测试压缩
        print("\n--- 测试压缩 ---")
        large_data = np.random.rand(500)
        await client.write("/my_group/compressed_data", large_data, compression="gzip")
        read_compressed = await client.read("/my_group/compressed_data")
        assert np.array_equal(large_data, read_compressed)
        print("压缩数据写入和读取验证成功。")

        # 5. 测试带去重功能的追加（适用于结构化数据）
        print("\n--- 测试带去重功能的追加 ---")
        # 创建一个结构化数组（类似于 pandas DataFrame）
        stock_dtype = np.dtype([('timestamp', np.int64), ('price', np.float32)])
        initial_stock_data = np.array([(1672531200, 150.0), (1672617600, 151.5)], dtype=stock_dtype)
        
        await client.write("/my_group/stocks", initial_stock_data)
        
        # 准备包含重复时间戳的新数据
        new_stock_data = np.array([(1672617600, 152.0), (1672704000, 153.0)], dtype=stock_dtype)
        
        # 使用 'timestamp' 字段去重追加
        await client.append("/my_group/stocks", new_stock_data, deduplicate_on='timestamp')
        
        read_deduped = await client.read("/my_group/stocks")
        
        # 验证：重复的时间戳被更新，新时间戳被添加
        expected_data = np.array([(1672531200, 150.0), (1672617600, 152.0), (1672704000, 153.0)], dtype=stock_dtype)
        assert np.array_equal(read_deduped, expected_data)
        print("带去重功能的追加操作验证成功。")

        # 6. 清理数据
        print("\n--- 清理数据 ---")
        await client.delete("/my_group")
        assert await client.read("/my_group") is None
        print("清理验证成功。")

    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## 运行测试

要运行集成测试，请确保服务器**未在运行**，然后在项目根目录执行 `pytest`：

```bash
pytest
```

测试套件会自动管理用于测试的服务器实例的启动和关闭。

## 贡献

欢迎贡献！如果您有改进的想法、新功能建议或发现任何问题，请随时创建 Issue 或提交 Pull Request。
