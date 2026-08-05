"""Encrypted-model inference with MagicLock.

Encrypt the model once:                加密一次即可：
    magiclock protect-model models/face.onnx   # -> models/face.onnx.enc

Then load it at runtime — the plaintext weights exist in memory only,
never on disk.                          运行时加载——明文权重只存在于内存，永不落盘。

Docs / 文档: https://magiclock.net/docs
"""

import magiclock
import onnxruntime

magiclock.bootstrap()  # brings the gate up against this machine's license

model_bytes = magiclock.open_model("models/face.onnx.enc")
session = onnxruntime.InferenceSession(model_bytes)

print("model loaded — inputs:", [i.name for i in session.get_inputs()])
