# demo_status.py
# Modified: 2025-10-13 16:12:24

import lazyImporter


def check_modules():
    """检查模块加载状态"""
    print("=== 模块状态检查 ===")

    # 测试一些模块
    modules_to_test = ['np', 'pd', 'requests', 'os', 'json']

    for module_alias in modules_to_test:
        try:
            # 尝试访问模块属性来触发加载
            if module_alias == 'np':
                _ = np.__version__
            elif module_alias == 'pd':
                _ = pd.__version__
            elif module_alias == 'requests':
                _ = requests.__version__
            elif module_alias == 'os':
                _ = os.name
            elif module_alias == 'json':
                _ = json.__name__

            print(f"✅ {module_alias}: 已加载")
        except Exception as e:
            print(f"❌ {module_alias}: 加载失败 - {e}")


def demonstrate_usage():
    """演示模块使用"""
    print("\n=== 模块使用演示 ===")

    try:
        # 使用numpy创建数组
        print("1. 使用NumPy:")
        data = np.array([[1, 2], [3, 4]])
        print(f"创建的数组:\n{data}")

        # 使用pandas创建DataFrame
        print("\n2. 使用Pandas:")
        df = pd.DataFrame(data, columns=['A', 'B'])
        print(f"创建的DataFrame:\n{df}")

        # 使用os模块
        print("\n3. 使用OS模块:")
        current_dir = os.getcwd()
        print(f"当前工作目录: {current_dir}")

        # 使用json模块
        print("\n4. 使用JSON模块:")
        sample_data = {"name": "测试", "values": [1, 2, 3]}
        json_str = json.dumps(sample_data, ensure_ascii=False, indent=2)
        print(f"JSON输出:\n{json_str}")

    except Exception as e:
        print(f"使用演示失败: {e}")


def test_auto_install():
    """测试自动安装功能（如果需要）"""
    print("\n=== 自动安装测试 ===")

    # 尝试使用一个可能未安装的模块
    try:
        # 注册一个可能未安装的模块
        lazy_imports._global_importer.register('yaml', 'pyyaml')

        # 现在尝试使用它（如果未安装会自动安装）
        print("尝试使用yaml模块...")
        data = yaml.dump({"test": "auto_install"}, default_flow_style=False)
        print("✅ yaml模块使用成功!")

    except Exception as e:
        print(f"yaml模块测试: {e}")


if __name__ == "__main__":
    print("🚀 惰性导入演示脚本启动")
    check_modules()

    # 演示模块使用
    demonstrate_usage()

    # 测试自动安装
    test_auto_install()

    print("\n🎉 演示完成!")
