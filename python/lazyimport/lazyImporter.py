"""
惰性导入模块 (Lazy Imports)
支持预注册模块、自动安装缺失依赖、直接全局访问
Modified: 2025-10-13 14:56:08
"""

import importlib
import inspect
import subprocess
import sys
from types import ModuleType


class LazyImporter:
    """
    惰性导入器主类
    功能：
    1. 预注册常用模块
    2. 按需加载模块（第一次使用时才导入）
    3. 自动安装缺失的依赖包
    4. 将模块注入全局命名空间供直接访问
    """

    # 预定义的模块映射字典
    _DEFAULT_MODULES = {
        'np': 'numpy',
        'pd': 'pandas',
        'plt': 'matplotlib.pyplot',
        'sns': 'seaborn',
        'tf': 'tensorflow',
        'torch': 'torch',
        'sklearn': 'sklearn',
        'requests': 'requests',
        'cv2': 'opencv-python',
        'PIL': 'PIL',
        'json': 'json',
        'os': 'os',
        'sys': 'sys',
        're': 're',
        'math': 'math',
        'random': 'random',
        'datetime': 'datetime',
        'time': 'time',
    }

    def __init__(self, custom_modules=None, inject_globals=True):
        """
        初始化惰性导入器

        Args:
            custom_modules (dict, optional): 自定义模块映射
            inject_globals (bool): 是否注入到全局命名空间
        """
        self._modules = {}
        self._register_defaults()

        if custom_modules:
            self.register_multiple(custom_modules)

        if inject_globals:
            self._inject_to_globals()

    def _register_defaults(self):
        """注册预定义的默认模块"""
        for alias, module_path in self._DEFAULT_MODULES.items():
            self._modules[alias] = (module_path, None)

    def _inject_to_globals(self):
        """
        将模块别名注入到调用者的全局命名空间
        使用更可靠的方法查找调用者
        """
        try:
            # 方法1: 使用inspect模块查找调用者
            frame = inspect.currentframe()
            # 向上回溯调用栈，找到真正调用我们的模块
            for i in range(10):  # 增加回溯层数以提高稳定性
                frame = frame.f_back
                if frame is None:
                    break
                # 检查这是模块级别的调用, 并且不是我们自己这个模块
                if frame.f_code.co_name == '<module>' and frame.f_globals.get('__name__') != __name__:
                    caller_globals = frame.f_globals
                    self._do_injection(caller_globals)
                    return

            # 方法2: 如果找不到，使用主模块
            caller_globals = sys.modules['__main__'].__dict__
            self._do_injection(caller_globals)

        except Exception as e:
            print(f"⚠️ 警告: 全局命名空间注入失败: {e}")

    def _do_injection(self, globals_dict):
        """执行实际的注入操作"""
        for alias in self._modules.keys():
            if alias not in globals_dict:
                globals_dict[alias] = _LazyModuleProxy(self, alias)

    def register(self, alias, module_path):
        """注册单个模块"""
        self._modules[alias] = (module_path, None)
        self._inject_single_to_globals(alias)
        return self

    def _inject_single_to_globals(self, alias):
        """将单个模块注入到全局命名空间"""
        try:
            frame = inspect.currentframe()
            for i in range(5):
                frame = frame.f_back
                if frame is None:
                    break
                if frame.f_code.co_name == '<module>':
                    caller_globals = frame.f_globals
                    if alias not in caller_globals:
                        caller_globals[alias] = _LazyModuleProxy(self, alias)
                    return
        except Exception:
            pass

    def register_multiple(self, modules_dict):
        """批量注册多个模块"""
        for alias, module_path in modules_dict.items():
            self._modules[alias] = (module_path, None)
        for alias in modules_dict.keys():
            self._inject_single_to_globals(alias)
        return self

    def _install_package(self, package_name):
        """尝试使用pip安装指定的包"""
        print(f"🔧 检测到缺失依赖，尝试安装: {package_name}")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"✅ 成功安装: {package_name}")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ 安装失败: {package_name}")
            return False

    def get_module(self, alias):
        """获取实际的模块对象"""
        if alias not in self._modules:
            available = list(self._modules.keys())
            raise AttributeError(f"模块 '{alias}' 未注册。可用模块: {available}")

        module_path, module_obj = self._modules[alias]

        if module_obj is None:
            try:
                module_obj = importlib.import_module(module_path)
                self._modules[alias] = (module_path, module_obj)
                print(f"📦 已加载模块: {alias} -> {module_path}")
            except ImportError as original_error:
                if self._install_package(module_path):
                    try:
                        module_obj = importlib.import_module(module_path)
                        self._modules[alias] = (module_path, module_obj)
                        print(f"✅ 成功导入已安装的模块: {alias}")
                    except ImportError:
                        raise ImportError(f"已安装 {module_path}，但导入仍失败: {original_error}")
                else:
                    raise ImportError(f"无法自动安装 {module_path}，请手动执行: pip install {module_path}")

        return module_obj

    def list_modules(self):
        """列出所有已注册的模块"""
        return list(self._modules.keys())

    def is_loaded(self, alias):
        """检查模块是否已加载"""
        if alias not in self._modules:
            return False
        return self._modules[alias][1] is not None


class _LazyModuleProxy:
    """惰性模块代理类"""

    def __init__(self, importer, alias):
        self._importer = importer
        self._alias = alias
        self._module = None

    def __getattr__(self, name):
        if self._module is None:
            self._module = self._importer.get_module(self._alias)
        return getattr(self._module, name)


# 创建全局导入器
def setup_lazy_imports(custom_modules=None):
    """
    设置惰性导入（推荐使用这个函数）

    Args:
        custom_modules (dict, optional): 自定义模块映射

    Returns:
        LazyImporter: 导入器实例
    """
    importer = LazyImporter(custom_modules, inject_globals=True)
    return importer


# 自动设置全局导入器
_global_importer = setup_lazy_imports()
