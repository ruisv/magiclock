<div align="center">

<img src="assets/logo.png" alt="MagicLock logo" width="96" height="96" />

# MagicLock — Python 源码加密与 AI 模型保护

**你的代码和模型，只在你授权的设备上运行——许可校验全程离线。**

[官网](https://magiclock.net) · [文档](https://magiclock.net/zh-Hans/docs) · [价格](https://magiclock.net/zh-Hans/pricing) · [English README](README.md)

![Python 3.9–3.14](https://img.shields.io/badge/python-3.9%E2%80%933.14-blue)
![Platforms](https://img.shields.io/badge/%E5%B9%B3%E5%8F%B0-macOS%20%C2%B7%20Windows%20%C2%B7%20Linux-lightgrey)
![Runtime network](https://img.shields.io/badge/%E8%BF%90%E8%A1%8C%E6%97%B6%E8%81%94%E7%BD%91-%E4%B8%8D%E9%9C%80%E8%A6%81-success)
![Free trial](https://img.shields.io/badge/%E5%85%8D%E8%B4%B9%E8%AF%95%E7%94%A8-48%E5%B0%8F%E6%97%B6%C2%B7%E5%85%8D%E7%BB%91%E5%8D%A1-orange)
![6 种语言](https://img.shields.io/badge/CLI%20%E4%B8%8E%E9%97%A8%E6%88%B7-6%20%E7%A7%8D%E8%AF%AD%E8%A8%80-blueviolet)

</div>

---

MagicLock 是一款商业化的 **Python 源码加密**、**AI 模型加密**与**软件授权（License）**工具。一条命令，把你的 `.py` 文件和模型权重变成加密产物——导入和运行与普通 Python 毫无二致，但只在你授权的机器上生效。验证与解密**全程离线**：无需加密狗，无需自己维护授权服务器，运行时不发起任何网络请求。

<p align="center">
  <img src="assets/terminal-demo.svg" alt="终端演示：magiclock protect 把 app.py 加密为 app.pya，magiclock run 正常运行；同一文件拷到未授权机器上则拒绝解密" width="760" />
</p>

> 这里是 MagicLock 在 GitHub 上的官方仓库：文档入口、可运行示例和公开的 issue 跟踪。MagicLock 本体是商业闭源软件，请前往 [magiclock.net](https://magiclock.net) 获取。

## 为什么用 MagicLock 做 Python 代码保护

- **一条命令，零改动接入。** `magiclock protect app.py` 直接加密源码。没有装饰器、没有注解、不动构建系统——每个受保护模块在执行第一行代码之前都要先通过运行时关卡。
- **模型只在内存中解密，别处一律不行。** 权重只加密一次，然后逐台密封到每一台授权设备。只在推理的那一刻、在内存中解开——明文从不落盘，解密密钥永不离开设备（任何服务器都交不出来，包括 MagicLock 自己的）。
- **授权，就是这台机器本身。** 只需在线激活一次；此后每次运行都在本地瞬间通过五道关卡——真实性、有效性、设备指纹、权益、新鲜度——**零网络连接**。
- **两档保护强度。** 便捷档（`.pya` 加密产物）无需编译器；编译档（`magiclock build`）把授权关卡织入**每一个模块**并编译为原生机器码——不再有明文 Python 出厂，也没有任何单点检查可供查找和剔除。
- **两个交付承诺，按产物二选一。** 默认产物**永远离线**——没有任何人能远程叫停它；加 `--web-gate` 的产物带**云端开关**：在门户里拨一下，它在所有部署点的下一次检查时停下；拨回来又恢复运行——无需重新交付。
- **交付出去的东西一直能用。** 订阅只管**打包新产物**，不管解密。订阅到期后，已经交付给用户的应用照常运行。
- **AI 协作就绪。** 一条 `magiclock skill`，让项目里的任何 AI 编程助手（包括 Claude Code）自己学会加密你的代码和模型。
- **说你的语言。** CLI 与门户支持 English、简体中文、繁體中文、日本語、한국어、Français。

## 快速上手：两条命令加密 Python 代码

```shell
pip install magiclock

# 第一次运行会引导登录并激活本机，然后完成加密。
magiclock protect app.py     # -> app.pya（加密产物）
magiclock run app.pya        # 和 `python app.py` 运行效果完全一致

# 指向目录即可递归保护整个项目：
magiclock protect src/
```

这就是全部工作流。`.pya` 是普通文件——按你现有的方式提交、拷贝、分发即可。落到未授权的机器上，它解不出任何东西。

## 加密 AI 模型

```shell
magiclock protect-model models/face.onnx    # -> models/face.onnx.enc
```

```python
import magiclock
import onnxruntime

magiclock.bootstrap()                                        # 依据本机授权拉起运行时关卡
model_bytes = magiclock.open_model("models/face.onnx.enc")   # 明文只存在于内存
session = onnxruntime.InferenceSession(model_bytes)
```

`open_model()` 不关心信封里装的是什么——ONNX、PyTorch state dict、原始权重、数据集、配置包都行。字节进、字节出，永不落盘。

## 把 Python 编译成原生二进制——最强档

```shell
pip install "magiclock[build]"

magiclock build app.py                       # 单个原生模块（.so / .pyd）
magiclock build app.py --standalone          # 自包含应用目录
magiclock build app.py --model weights.onnx  # 把加密模型一并打进构建产物
```

`magiclock build` 会遍历入口可达的每一个 `.py` 模块，逐个插入授权关卡，再整体编译为原生代码。产物在运行机器上**无需安装 MagicLock、无需账号、无需联网**。

## 有效期、试用与更强的锁

```shell
magiclock protect app.py --expires-in 30d       # 产物 30 天后拒绝解密
magiclock protect app.py --expires-at 2026-12-31
magiclock protect app.py --trial                # 48 小时自毁——演示 / 评估专用
magiclock protect app.py --lock-passphrase      # 机器 + 口令双因子锁
magiclock protect app.py --no-bind-machine --emit-key   # 便携模式：凭密钥解锁，不绑机器
```

## 远程停用已交付的软件——云端开关（`--web-gate`）

```shell
magiclock protect app.py --web-gate
```

云控产物在运行前会先征得你的批准。在门户里把开关拨下，它在所有部署点的下一次检查时停止运行；拨回来立即恢复——无需重新交付。断网时它会在**你自己设定**的宽限期内（1 小时到 30 天）继续运行。为租赁、订阅制、限期试点、催收欠款而生。

不加该参数的产物则永远离线，任何人都无法远程吊销——两个承诺都是绝对的。而且是按产物选择，不是按账号：一条产品线里可以两种混用。

## MagicLock vs PyArmor、SOURCEdefender、Nuitka、Cython、PyInstaller

| | **MagicLock** | 混淆器（如 PyArmor） | 加密加载器（如 SOURCEdefender） | 编译器（Nuitka、Cython） | 打包器（PyInstaller） |
|---|---|---|---|---|---|
| 思路 | 加密 + 设备绑定授权 + 可选原生编译 | 字节码混淆 | AES 加密 `.py` 后加载 | 编译为 C / 原生代码 | 打包成可执行文件 |
| 需要改代码 | **不需要** | 一般不需要 | 不需要 | 不需要 | 不需要 |
| 设备绑定（节点锁）授权 | **内置** | 视版本而定 | — | — | — |
| AI 模型 / 资源加密 | **内置，逐设备信封** | — | — | — | — |
| 激活后完全离线运行 | **是** | 视情况 | 视情况 | 不适用（无授权层） | 不适用（无授权层） |
| 远程叫停（可选开启） | **有** | — | — | — | — |
| 限时 / 自毁产物 | **有** | 视版本而定 | 有 | — | — |
| 多语言 CLI 与门户 | **原生支持 6 种语言**——英 · 简中 · 繁中 · 日 · 韩 · 法 | 视情况 | — | — | — |
| 保护强度上限 | 原生机器码 + **每个模块**都有关卡 | 混淆字节码（原理上可还原） | 加载时解回字节码 | 原生代码，但**没有授权层** | 打包体可轻易解开 |

编译器和打包器解决的是分发问题，不是保护和授权；混淆花足够功夫就能还原。MagicLock 把加密、节点锁授权、原生编译合为一个工具，还补上了上面谁都没有的两样：逐设备的模型加密，和远程叫停开关。

### MagicLock vs PyArmor

PyArmor 是最知名的 Python **混淆器**：把脚本变换成混淆字节码，付费版提供机器绑定。但混淆本质上还是把完整程序交到了拿到文件的人手里——花足够功夫就能还原。MagicLock 走的是**加密**路线：在未授权机器上没有东西可供逆向，只有密文。混淆做不到的事 MagicLock 也补上了——逐设备的 AI 模型加密、可选的远程叫停开关；编译档更是直接出厂原生机器码，每个模块都织入授权关卡。

### MagicLock vs SOURCEdefender

SOURCEdefender 用 AES 加密 `.py` 文件、在导入时解密，支持限时脚本。它回答的是"别人能不能读我的源码"，而不是"谁有权运行它"——没有设备绑定，没有模型加密，交付之后也没有任何干预手段。MagicLock 补上了节点锁授权（产物在未授权机器上拒绝解密）、逐设备的 AI 模型信封、原生编译档，以及可选的云端开关。

### MagicLock vs Nuitka / Cython

Nuitka 和 Cython 把 Python **编译**成 C 和原生代码——性能出色，也确实提高了阅读门槛，但它们不是授权工具：二进制拿到就能跑、永远能跑，随包分发的模型权重更是明文躺在旁边。MagicLock 的编译档同样基于原生编译，然后补上编译器不管的部分：每个模块的授权关卡、设备绑定、模型加密、有效期。

### MagicLock vs PyInstaller

PyInstaller 解决的是**打包**，不是保护：把应用和解释器捆成一个可执行文件，但用公开工具就能轻易解回 `.pyc` 字节码——它本来就不是为保密设计的。MagicLock 的产物不管文件流落到哪里都保持加密，只在你授权的设备上才能变成一个能运行的程序。两者完全可以搭配：先用 MagicLock 保护，再按你喜欢的方式打包。

## 常见问题

**运行受保护的应用需要联网吗？**
不需要。只在激活时在线一次；此后受保护的代码和模型都在授权机器上完全离线验证与解密。

**订阅到期后会怎样？**
已经交付的一切照常运行——订阅只限制打包**新**产物，不影响解密。想继续发布时再续订即可。

**能远程停用已经交付出去的应用吗？**
能——前提是加密时选择了 `--web-gate`。这类产物听门户里那个开关的。不加该参数的产物永远离线、永远无法被远程吊销——两个方向的承诺都是绝对的。

**我的最终用户需要 MagicLock 账号吗？**
不需要。你按自己的方式交付受保护的应用；用户不需要账号、不需要安装（编译档产物甚至完全不需要装 MagicLock 包）。

**我的源码或模型会被上传吗？**
不会。`protect`、`protect-model`、`build` 全部在本地执行。模型只在授权设备的内存中解密，解密密钥永不离开设备——从不上传、从不托管，任何服务器都交不出来。

**免费试用是真免费吗？**
真免费——全部能力免费用 48 小时，1 台设备，无需绑卡。计时从你第一次激活机器开始，而不是注册时。到期后已构建的一切照常运行，只是要订阅后才能继续打包新产物。

**支持哪些 Python 版本和平台？**
Python 3.9–3.14，macOS（Apple Silicon）、Windows、Linux。

**和混淆有什么区别？**
混淆只是变换代码，整个程序仍然完整交到了攻击者手里。MagicLock 是加密——在未授权的机器上没有东西可供逆向，只有密文。编译档更进一步：原生机器码，且每个模块都织入了授权关卡。

## 链接

- 🌐 官网：**[magiclock.net](https://magiclock.net/zh-Hans)**
- 📚 文档：**[magiclock.net/zh-Hans/docs](https://magiclock.net/zh-Hans/docs)**
- 💰 价格（48 小时免费试用、订阅、买断）：**[magiclock.net/zh-Hans/pricing](https://magiclock.net/zh-Hans/pricing)**
- 🐛 Bug 与提问：直接在本仓库[提 issue](../../issues)

## 许可

**本仓库**中的文档与示例代码采用 MIT 许可（见 [LICENSE](LICENSE)）。MagicLock 本体为商业专有软件——详见 [magiclock.net/zh-Hans/pricing](https://magiclock.net/zh-Hans/pricing)。
