# UI 自动化测试框架

基于 **Playwright** + **Python** + **Pytest** 构建的企业级 UI 自动化测试框架。

## 概述

这是一个现代化、可扩展、易维护的 UI 自动化测试解决方案，专为企业级应用设计。框架遵循行业最佳实践，包括页面对象模型（POM）模式、分层架构和数据驱动测试。

## 技术栈

| 类别 | 技术 |
|------|------|
| 测试框架 | Playwright 1.40 |
| 编程语言 | Python 3.9+ |
| 测试运行器 | Pytest 7.2+ |
| 测试报告 | Pytest HTML |
| 数据验证 | Pydantic 2.5 |
| 配置文件 | PyYAML |

## 项目架构

```
Web_UI_Auto/
├── core/                       # 核心层
│   ├── base_page.py           # BasePage - 页面对象模型基类
│   ├── logger.py              # 日志工具
│   ├── custom_assertions.py  # 自定义断言方法
│   └── data_models.py        # Pydantic 数据模型
├── pages/                      # 页面对象层
│   ├── login_page.py          # 登录页面对象
│   ├── dashboard_page.py      # 仪表盘页面对象
│   └── components/            # 可复用组件
├── tests/                      # 测试用例层
│   ├── conftest.py            # Pytest Fixtures 配置
│   └── smoke/
│       └── test_login.py      # 登录功能测试
├── data/                       # 数据层
│   ├── users.json             # 用户测试数据
│   ├── config.yaml            # 环境配置文件
│   └── demo_app.html          # 测试用 Demo 应用
├── helpers/                    # 辅助工具
│   └── data_generator.py      # 测试数据生成器
├── reports/                    # 测试报告目录
├── screenshots/               # 失败截图目录
├── traces/                     # Playwright trace 文件
├── pytest.ini                 # Pytest 配置
├── requirements.txt           # Python 依赖
└── .env                      # 环境变量
```

## 核心特性

### 设计原则

- **健壮性**：智能等待机制，避免不稳定测试
- **可维护性**：清晰的代码架构，基于 POM 模式
- **可扩展性**：模块化设计，便于功能扩展

### 主要功能

- 页面对象模型（POM）架构
- 基于 JSON/YAML 的数据驱动测试
- 多环境支持（staging、production、development、demo）
- 失败时自动截图
- Playwright trace 查看器支持
- 完整的 HTML 测试报告
- 自定义断言库
- 测试数据生成工具

## 安装指南

### 环境要求

- Python 3.9+
- pip

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/cylDemo/Web_UI_Auto.git
cd UI_Auto_demo

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

## 配置说明

### 环境变量 (.env)

```env
BASE_URL=https://staging.example.com
HEADLESS=false
CI=false
TIMEOUT=30000
RETRY_COUNT=2
PARALLEL_WORKERS=4
ENV=demo
```

### 环境配置 (data/config.yaml)

支持的环境：`staging`、`production`、`development`、`demo`

## 使用方法

### 运行所有测试

```bash
python -m pytest tests/smoke/test_login.py -v
```

### 按标记运行

```bash
# 仅运行冒烟测试
python -m pytest -m smoke -v

# 仅运行回归测试
python -m pytest -m regression -v

# 按优先级运行
python -m pytest -m P0 -v
```

### 生成 HTML 报告

```bash
python -m pytest --html=reports/pytest-report.html --self-contained-html
```

### 并行执行

```bash
python -m pytest -n 4
```

## 测试用例

### 登录测试（冒烟）

| 测试用例 | 优先级 | 描述 |
|---------|--------|------|
| `test_login_success` | P0 | 使用有效凭证登录成功 |
| `test_login_page_elements` | P0 | 验证登录页面所有元素可见 |
| `test_login_button_state` | P0 | 验证登录按钮处于启用状态 |

### 登录测试（回归）

| 测试用例 | 优先级 | 描述 |
|---------|--------|------|
| `test_login_failed_with_invalid_password` | P1 | 验证无效密码错误提示 |
| `test_login_failed_with_nonexistent_user` | P1 | 验证不存在用户错误提示 |
| `test_login_empty_fields` | P2 | 验证空用户名/密码校验 |

### 仪表盘测试

| 测试用例 | 优先级 | 描述 |
|---------|--------|------|
| `test_dashboard_elements_visible` | P2 | 验证登录后仪表盘元素可见 |
| `test_logout` | P2 | 验证退出登录功能 |

## 测试数据

### 有效用户凭证

```json
{
  "username": "testuser@example.com",
  "password": "Test123456"
}
```

### Demo 应用

框架包含一个位于 `data/demo_app.html` 的演示登录应用，用于测试目的。

## 分层架构详解

### 核心层 (`core/`)

- **base_page.py**: 所有页面对象的基类，提供通用方法
- **logger.py**: 集中化日志配置
- **custom_assertions.py**: 可复用的断言方法
- **data_models.py**: Pydantic 数据验证模型

### 页面对象层 (`pages/`)

- **login_page.py**: 登录页面定位器和操作方法
- **dashboard_page.py**: 仪表盘页面定位器和操作方法

### 测试层 (`tests/`)

- **conftest.py**: Pytest fixtures、钩子和配置
- **test_login.py**: 登录功能测试用例

### 数据层 (`data/`)

- **users.json**: 用户凭证和测试数据
- **config.yaml**: 环境特定配置

## CI/CD 集成

### GitHub Actions 示例

```yaml
name: UI 自动化测试
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: 安装依赖
        run: |
          pip install -r requirements.txt
          playwright install chromium
      - name: 运行测试
        run: pytest --workers=4
```

## 最佳实践

1. **始终使用页面对象模型** - 测试文件中禁止直接写 `page.locator()`
2. **禁止硬编码数据** - 使用 JSON/YAML 文件管理测试数据
3. **智能等待** - 使用 Playwright 自动等待替代 `time.sleep()`
4. **命名规范** - 使用清晰描述性的测试名称
5. **原子性测试** - 每个测试应相互独立
6. **失败截图** - 启用自动截图捕获

## 质量指标

| 指标 | 目标 |
|------|------|
| 通过率 | >= 98% |
| 执行时间 | < 15 分钟（完整套件）|
| 不稳定率 | < 2% |
| 代码覆盖率 | >= 80% |

## 贡献指南

1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT 许可证

## 技术支持

如有问题，请在 GitHub 上提交 Issue。
