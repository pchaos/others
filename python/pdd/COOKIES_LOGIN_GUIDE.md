# 🍪 Cookies登录测试指南

## 📁 脚本位置

所有Cookies测试脚本已移动到 `tests/` 目录：

```bash
tests/
├── test_cookies_quick.py      # ⭐ 推荐 - 快速测试版（60秒超时）
├── test_cookies_manual.py     # 手动关闭版（无限等待）
├── test_cookies_simple.py     # 简单版
├── test_cookies_keep_open.py  # 保持打开版（详细输出）
└── test_cookies_login.py      # 详细测试版
```

## 🚀 快速开始

### 前置条件
确保已有cookies文件：
```bash
# 检查cookies文件
ls -la .pdd_cookies.json

# 如果没有，先运行主程序生成cookies
python pdd_order_scraper_optimized.py
```

### 运行测试脚本

#### 方法1: 从项目根目录运行
```bash
# 推荐：使用快速测试版（60秒超时演示）
python tests/test_cookies_quick.py

# 或使用完全手动版（无限等待）
python tests/test_cookies_manual.py
```

#### 方法2: 进入tests目录运行
```bash
cd tests
python test_cookies_quick.py
python test_cookies_manual.py
```

## 📖 脚本说明

### 1. test_cookies_quick.py ⭐ 推荐
**功能**: 快速测试cookies登录
**特点**: 
- 60秒演示超时自动关闭
- 界面简洁清晰
- 适合快速验证cookies是否有效

**使用方法**:
```bash
python tests/test_cookies_quick.py
```

**输出示例**:
```
🧪 快速测试：登录后保持浏览器打开
============================================================
✅ 找到cookies文件
📱 打开拼多多...
🔐 登录中...
✅ 登录成功！
✅ 登录状态确认

============================================================
🎉 登录成功！
📱 页面: https://mobile.pinduoduo.com/personal.html

💡 现在浏览器已打开，您可以：
   - 查看订单列表
   - 点击查看详情
   - 慢慢浏览

⚠️  请手动关闭浏览器窗口来退出程序
============================================================

⏳ 等待浏览器关闭（演示60秒超时）...
⏰ 演示超时，关闭浏览器
```

### 2. test_cookies_manual.py ⭐ 推荐新手
**功能**: 手动关闭浏览器版本
**特点**: 
- 登录成功后无限期等待
- 直到您手动关闭浏览器
- 适合慢慢浏览订单

**使用方法**:
```bash
python tests/test_cookies_manual.py
```

### 3. 其他脚本

| 脚本 | 特点 | 适用场景 |
|------|------|----------|
| `test_cookies_simple.py` | 简洁版 | 简单测试 |
| `test_cookies_keep_open.py` | 详细输出 | 调试查看 |
| `test_cookies_login.py` | 详细测试 | 深入测试 |

## 💡 使用流程

1. **运行脚本**
   ```bash
   python tests/test_cookies_quick.py
   ```

2. **等待登录**
   - 脚本自动使用cookies登录
   - 如果成功，浏览器会打开拼多多页面
   - 显示登录成功信息

3. **您操作页面**
   - 📋 查看订单列表
   - 🔍 点击订单查看详情
   - 📊 浏览历史订单
   - 🛒 继续购物

4. **关闭浏览器退出**
   - **手动关闭浏览器窗口**
   - 程序自动检测并退出
   - 不需要使用Ctrl+C

## 🔧 常见问题

### Q1: 提示cookie文件不存在？
**解决**: 先运行主程序生成cookies
```bash
python pdd_order_scraper_optimized.py
```

### Q2: 登录失败，cookies无效？
**解决**: 
1. 删除旧的cookies文件
2. 重新运行主程序登录
```bash
rm .pdd_cookies.json
python pdd_order_scraper_optimized.py
```

### Q3: 脚本报错"ModuleNotFoundError"?
**解决**: 确保从项目根目录运行
```bash
cd /home/user/myDocs/YUNIO/tmp/gupiao/others/python/pdd
python tests/test_cookies_quick.py
```

### Q4: 程序卡住不动？
**解决**: 这是正常现象，程序在等待您关闭浏览器
- 手动关闭浏览器窗口即可退出
- 或等待60秒超时（快速测试版）

### Q5: 如何强制退出？
**解决**: 
- 关闭浏览器窗口（推荐）
- 或按 `Ctrl+C` 强制中断程序

## 📊 功能特点

✅ **简单易用** - 无需复杂操作
✅ **自动登录** - 使用已保存的cookies
✅ **手动控制** - 浏览器打开后可自由操作
✅ **智能检测** - 自动检测登录状态
✅ **灵活等待** - 直到用户关闭浏览器

## 📝 注意事项

1. 请确保cookies文件存在且有效
2. 登录成功后会打开浏览器窗口
3. **必须手动关闭浏览器**才能退出程序
4. 如果cookies过期，需要重新登录生成

## 🔗 相关文件

- **主程序**: `pdd_order_scraper_optimized.py`
- **登录模块**: `pdd_login.py`
- **Cookies文件**: `.pdd_cookies.json` (自动生成)

## 🎯 使用建议

### 场景1: 快速验证
```bash
# 快速测试cookies是否有效
python tests/test_cookies_quick.py
```

### 场景2: 慢慢浏览
```bash
# 登录后慢慢挑选商品
python tests/test_cookies_manual.py
```

### 场景3: 调试问题
```bash
# 查看详细日志
python tests/test_cookies_login.py
```

---

**💡 提示**: 这些测试工具非常适合验证cookies是否正常工作，以及在登录后慢慢浏览订单详情！

**📌 记住**: 登录后**手动关闭浏览器窗口**来退出程序！
