"""回测 Schema 导入测试。

本文件用于验证回测 Schema 模块可以正常导入，
避免模型声明阶段因字段名与类型名冲突导致应用启动失败。
"""

import importlib
import sys


def test_backtest_schema_module_can_be_imported() -> None:
    """验证回测 Schema 模块可正常导入。

    入参：
        无。

    出参：
        None。
    """
    sys.modules.pop("app.schemas.backtest", None)

    module = importlib.import_module("app.schemas.backtest")

    assert hasattr(module, "BacktestRunResponse")
