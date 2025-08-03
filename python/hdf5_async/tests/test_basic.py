# tests/test_basic.py
import pytest
from server.server import HDF5Server
import numpy as np
from client.client import HDF5Client


@pytest.mark.asyncio
async def test_server_initialization(hdf5_server):
    """
    测试服务端是否能成功初始化和启动。
    这个测试依赖于 conftest.py 中的 hdf5_server fixture。
    """
    server_instance, host, port = hdf5_server

    # 1. 验证 fixture 是否返回了正确的对象类型
    assert server_instance is not None, "服务器实例不应为 None"
    assert isinstance(server_instance, HDF5Server), "返回的应为 HDF5Server 实例"
    
    # 2. 验证服务器是否处于正在服务的状态
    assert server_instance.is_serving(), "服务器应该正在运行"
    
    # 3. 验证主机和端口信息的有效性
    assert isinstance(host, str) and host, "主机名应该是有效的字符串"
    assert isinstance(port, int) and port > 0, f"端口号 {port} 应该是一个有效的端口"

    print(f"\n服务端成功启动并正在监听 {host}:{port}")


@pytest.mark.asyncio
async def test_simple_write_and_read(hdf5_server):
    """
    测试连接到服务端，写入一个简单的数据集，然后读取并验证。
    """
    _server_instance, host, port = hdf5_server

    # 1. 初始化客户端并连接
    client = HDF5Client(host, port)
    await client.connect()
    print(f"\n客户端成功连接到 {host}:{port}")

    try:
        # 2. 准备并写入数据
        dataset_path = '/test/simple_write'
        data_to_write = np.random.rand(10, 5)
        
        await client.write(dataset_path, data_to_write)
        print(f"客户端: 成功请求写入数据到 {dataset_path}")

        # 3. 读取数据进行验证
        read_data = await client.read(dataset_path)
        
        print(f"客户端: 从 {dataset_path} 读取数据")

        # 4. 验证数据
        assert read_data is not None, "读取的数据不应为 None"
        assert np.array_equal(data_to_write, read_data), f"数据不匹配！\n期望:\n{data_to_write}\n实际:\n{read_data}"
        print("客户端: 数据验证成功")

    finally:
        # 5. 关闭连接
        await client.close()
        print("客户端: 连接已关闭")