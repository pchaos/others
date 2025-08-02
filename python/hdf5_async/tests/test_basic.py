# tests/test_basic.py
import pytest
from server.server import HDF5Server

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