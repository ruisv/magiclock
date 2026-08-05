#!/usr/bin/env bash
# MagicLock quickstart — protect a Python file and run it, start to finish.
# 快速上手——从加密到运行的完整流程。
# Docs / 文档: https://magiclock.net/docs
set -euo pipefail

pip install magiclock

cat > app.py <<'PY'
print("hello from a protected app")
PY

# First run signs you in and activates this machine, then encrypts.
# 第一次运行会引导登录并激活本机，然后完成加密。
magiclock protect app.py     # -> app.pya

# Runs exactly like `python app.py` — but only on machines you authorize.
# 运行效果与 `python app.py` 完全一致——但只在你授权的机器上生效。
magiclock run app.pya
