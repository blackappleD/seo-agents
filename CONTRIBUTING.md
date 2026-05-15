# 贡献指南

1. 安装开发依赖：

```bash
python -m pip install -e ".[dev]"
```

2. 运行检查：

```bash
python scripts/portability_check.py --json
python -m ruff check .
pytest -q
```

3. 贡献规则：

- parser、security、report contract、CLI 行为需要配套测试。
- optional dependency 不能在 import 阶段让程序退出。
- skill 文档必须与 CLI 实际能力一致。
- 用户可见文案默认使用中文；代码标识符和技术名词保留英文。
