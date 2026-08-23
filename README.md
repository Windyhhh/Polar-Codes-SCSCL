# ❄️ Polar 码 SCSCL 译码 | Polar Codes SCSCL Decoder

> **极化码的串行抵消列表译码实现——5G 信道编码核心算法，从理论到仿真的完整实现，误码率性能逼近 ML。**
>
> *Successive Cancellation Stack List decoding for Polar codes — core algorithm of 5G channel coding, complete implementation from theory to simulation, BER performance approaching ML.*

---

## ⭐ 核心卖点 | Why Star This

| 卖点 | Feature | 一句话 |
|------|---------|--------|
| 📡 **5G 标准** | 5G Standard | Polar 码是 5G eMBB 控制信道的标准编码方案 |
| 🔢 **SCSCL 译码** | SCSCL Decoder | 串行抵消栈列表译码，兼顾性能与复杂度 |
| 📊 **完整仿真** | Full Simulation | 从编码到译码到 BER 曲线的完整链路 |
| 🎯 **高性能** | High Performance | 列表译码性能逼近最大似然 (ML) |
| ⚡ **复杂度优化** | Complexity Opt | 栈结构减少不必要的路径扩展 |

---

## 🏆 技术栈 | Tech Stack

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![NumPy](https://img.shields.io/badge/NumPy-1.20+-orange?logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.4+-red?logo=plotly)
![SciPy](https://img.shields.io/badge/SciPy-1.7+-purple?logo=scipy)

---

## 📊 译码算法对比 | Decoder Comparison

| 算法 | 复杂度 | BER 性能 | 并行度 | 实现难度 |
|------|--------|---------|--------|---------|
| SC (串行抵消) | O(N log N) | 🟡 中等 | ❌ 低 | 🟢 简单 |
| SCL (SC 列表) | O(L·N log N) | ✅ 好 | ❌ 低 | 🟡 中等 |
| SCS (SC 栈) | O(N log N)~O(L·N log N) | 🟡 中 | ❌ 低 | 🟡 中等 |
| **SCSCL (本项目)** | **自适应** | **✅ 好** | **❌ 低** | **🔴 较难** |
| ML (最大似然) | O(2^N) | ✅ 最优 | ✅ 高 | 🔴 不可行 |

---

## 🚀 快速开始 | Quick Start

```bash
git clone https://github.com/Windyhhh/Polar-Codes-SCSCL.git
cd Polar-Codes-SCSCL
pip install -r requirements.txt

# 单次编解码测试
python main.py --N 1024 --K 512 --snr 2 --list-size 8

# BER 曲线仿真
python simulate.py --N 1024 --K 512 --snrs 0,1,2,3,4,5 --list-size 8 --frames 10000
```

---

## 📂 项目结构 | Project Structure

```
Polar-Codes-SCSCL/
├── main.py                    # 主入口
├── simulate.py                # BER 仿真
├── requirements.txt           # 依赖
├── encoder/
│   └── polar_encoder.py       # Polar 编码器
├── decoder/
│   ├── sc_decoder.py          # SC 译码器 (基线)
│   ├── scl_decoder.py         # SCL 译码器
│   ├── scs_decoder.py         # SCS 译码器
│   └── scscl_decoder.py       # SCSCL 译码器 (核心)
├── channel/
│   └── awgn.py                # AWGN 信道模型
├── construction/
│   └── polar_construction.py  # 极化信道构造
├── evaluation/
│   ├── ber.py                 # BER 计算
│   └── plot.py                # 曲线绘制
└── results/                   # 仿真结果
```

---

## 🔬 核心原理 | Core Idea

### 极化码编码 | Polar Encoding

```
输入: u (长度 N = 2^n 的信息比特 + 冻结比特)
编码: x = u · F_N

其中 F_N 是生成矩阵:
  F_1 = [1]
  F_2 = [[1,0],[1,1]]
  F_N = F_2 ⊗ F_{N/2}  (克罗内克积)

极化效应:
  - 经过信道极化后，部分信道趋近于无噪 (可靠信道)
  - 部分信道趋近于全噪 (不可靠信道)
  - 信息比特放在可靠信道，冻结比特放在不可靠信道
```

### SC 译码 | Successive Cancellation

```
SC 译码按顺序逐个判决比特:
  for i = 0 to N-1:
    L_i = 计算第 i 个比特的对数似然比 (LLR)
    if i 是信息比特:
      û_i = {0 if L_i > 0, 1 otherwise}
    else:
      û_i = 0 (冻结比特)

问题: 早期比特的错误会传播到后续比特 (错误传播)
```

### SCL 译码 | SC List

```
SCL 维护 L 个候选路径:
  for i = 0 to N-1:
    for each path in 当前列表:
      扩展为两个分支 (û_i = 0 和 û_i = 1)
      计算每个分支的路径度量 (PM)
    从 2L 个分支中选择 PM 最优的 L 个

优势: 保留多个候选，减少错误传播
复杂度: L 倍 SC 的复杂度
```

### SCSCL 译码 | SC Stack List

```
SCSCL 结合栈和列表的优势:
  - 使用栈结构优先扩展最有希望的路径
  - 维护列表大小 L，但不需要每次都扩展所有路径
  - 当栈顶路径的 PM 足够好时，可以提前终止
  - 平均复杂度低于 SCL，最坏情况等于 SCL

优势:
  - 平均复杂度低于 SCL
  - 性能与 SCL 相当
  - 适合对延迟敏感的场景
```

---

## 📊 性能指标 | Performance Metrics

| 指标 | 说明 |
|------|------|
| BER (误比特率) | 错误比特数 / 总比特数 |
| FER (误帧率) | 错误帧数 / 总帧数 |
| 复杂度 | 译码所需的运算量 |
| 延迟 | 从接收到译码完成的时间 |
| 列表大小 L | SCL/SCSCL 的路径数 |

---

## 🎯 应用场景 | Use Cases

- 📱 **5G 通信**：eMBB 控制信道的编码方案
- 🛰️ **卫星通信**：深空通信的高可靠编码
- 📡 **无线通信**：下一代通信系统的信道编码
- 🔬 **信息论**：信道极化理论的实验验证
- 🎓 **通信教学**：现代信道编码的教学案例

---

## 📚 参考文献 | References

- Arıkan, E. "Channel polarization: A method for constructing capacity-achieving codes for symmetric binary-input memoryless channels." IEEE Trans. Info. Theory 2009.
- Tal, I., & Vardy, A. "List decoding of polar codes." IEEE Trans. Info. Theory 2015.
- Niu, K., & Chen, K. "Stack decoding of polar codes." Electronics Letters 2012.
- 3GPP TS 38.212. "Multiplexing and channel coding." 2018.

---

## 📄 License

MIT License — 自由使用、修改和分发。

---

> 💡 **5G 标准 Polar 码的完整实现，Star ⭐ 支持开源通信！**
