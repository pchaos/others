# demo_status.py
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


if __name__ == "__main__":
    check_modules()
