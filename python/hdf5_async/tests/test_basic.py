# tests/test_basic.py
import pytest
from server.server import HDF5Server
import numpy as np
from client.client import HDF5Client
from common.config_manager import config_manager


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
async def test_get_config(hdf5_server):
    """
    测试客户端能否成功获取服务端配置。
    """
    _server_instance, host, port = hdf5_server
    client = HDF5Client(host, port)
    await client.connect()

    try:
        # The get_config call is implicitly done in connect, we can access the result
        # or make an explicit call if the client supports it.
        # Re-calling it explicitly to test the command handler.
        config = await client._send_request("get_config")
        
        assert config is not None, "配置信息不应为 None"
        assert config["status"] == "success", "获取配置请求应成功"
        assert "serialization_format" in config, "配置中应包含序列化格式"
        assert "use_compression" in config, "配置中应包含压缩设置"
        assert "debug" in config, "配置中应包含调试模式设置"

        # 验证配置值是否与服务器设置一致
        expected_serialization = config_manager.get('server', 'serialization_format')
        expected_compression = config_manager.getboolean('server', 'use_compression')
        expected_debug = config_manager.getboolean('server', 'debug')

        assert config["serialization_format"] == expected_serialization
        assert config["use_compression"] == expected_compression
        assert config["debug"] == expected_debug
        print("\n客户端: 成功获取并验证了服务端配置")

    finally:
        await client.close()


@pytest.mark.asyncio
async def test_is_connected(hdf5_server):
    """
    测试客户端 is_connected 方法的准确性。
    """
    _server_instance, host, port = hdf5_server
    client = HDF5Client(host, port)

    # 1. 连接前
    assert not client.is_connected(), "连接前 is_connected 应返回 False"
    print("\n客户端: 连接前状态正确 (is_connected=False)")

    # 2. 连接后
    await client.connect()
    assert client.is_connected(), "连接后 is_connected 应返回 True"
    print("客户端: 连接后状态正确 (is_connected=True)")

    # 3. 关闭后
    await client.close()
    assert not client.is_connected(), "关闭后 is_connected 应返回 False"
    print("客户端: 关闭后状态正确 (is_connected=False)")


@pytest.mark.asyncio
async def test_invalid_command(hdf5_server):
    """
    测试服务端对未知命令的响应。
    """
    _server_instance, host, port = hdf5_server
    client = HDF5Client(host, port)
    await client.connect()

    try:
        # 发送一个服务端不支持的命令
        response = await client.request({"command": "non_existent_command"})
        
        assert response is not None, "响应不应为 None"
        assert response.get("status") == "error", "状态应为 'error'"
        assert "Unknown command" in response.get("message", ""), "错误信息应包含 'Unknown command'"
        print("\n客户端: 成功接收到未知命令的错误响应")

    finally:
        await client.close()


@pytest.mark.asyncio
async def test_client_connection_error():
    """
    测试当服务器未运行时，客户端连接的异常处理。
    """
    # 使用一个未被占用的端口
    host = config_manager.get('server', 'host')
    port = 9999 # 假设这个端口没有服务在监听
    
    client = HDF5Client(host, port)
    
    with pytest.raises(ConnectionRefusedError) as excinfo:
        await client.connect()
    
    # Check for a more general part of the error message
    assert "refused" in str(excinfo.value).lower() or "connect call failed" in str(excinfo.value).lower(), "应捕获到 ConnectionRefusedError"
    print(f"\n客户端: 成功捕获到连接被拒绝的错误: {excinfo.value}")


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
