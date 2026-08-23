# 📡 Polar Codes SCSCL | 极化码 SCSCL 解码算法全解析

> **A complete Python implementation of 5G Polar Codes with SC, SCL, and CA-SCL decoding. Supports N=4 to N=128, CRC-aided list decoding, and BER performance analysis.**
>
> 5G 极化码完整 Python 实现，支持 SC、SCL、CA-SCL 三种解码算法。码长 N=4~128，CRC 辅助列表解码，误码率性能分析。

---

## 🌟 Why This Project? | 项目亮点

Polar codes, introduced by Arıkan in 2009, are the first provably capacity-achieving channel codes and were selected as the control channel coding standard for **5G NR (New Radio)**. This project provides a **complete, bug-fixed implementation** of polar codes with three decoding algorithms (SC, SCL, CA-SCL), multiple reliability ordering methods (GA, PW), and CRC-aided list decoding — all in pure Python with NumPy.

极化码由 Arıkan 于 2009 年提出，是第一种被证明可达信道容量的编码方案，并被选为 **5G NR（新空口）** 控制信道编码标准。本项目提供了一个**完整的、修复了关键 bug 的**极化码实现，包含三种解码算法（SC、SCL、CA-SCL）、多种可靠性排序方法（GA、PW）、CRC 辅助列表解码——全部使用纯 Python + NumPy 实现。

| Feature | Details |
|---------|---------|
| **Code Lengths** | N = 4, 8, 16, 32, 64, 128 (powers of 2) |
| **Decoding Algorithms** | SC (Successive Cancellation), SCL (SC List), CA-SCL (CRC-Aided SCL) |
| **Reliability Ordering** | GA (Gaussian Approximation), PW (Polarization Weight) |
| **CRC Support** | CRC-16-CCITT (polynomial 0x11021) |
| **List Sizes** | Configurable L = 2, 4, 8, 16, 32 |
| **Channel Model** | AWGN with BPSK modulation |
| **Performance Metrics** | BER (Bit Error Rate), end-to-end accuracy |
| **Dependencies** | NumPy only (no heavy frameworks) |

---

## 🏗️ Architecture | 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                      PolarConfig                              │
│  N (code length), K (info bits), design (GA/PW), SNR,      │
│  use_crc, crc_polynomial, use_scl, list_size                │
└──────────────────────────────┬──────────────────────────────┘
                               │
           ┌───────────────────┼───────────────────┐
           ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  PolarEncoder    │ │  PolarDecoder    │ │  PolarSystem     │
│                  │ │                  │ │                  │
│ • Reliability    │ │ • SC Decode      │ │ • AWGN Channel   │
│   ordering (GA/  │ │   (recursive)    │ │   simulation     │
│   PW)            │ │ • SCL Decode     │ │ • LLR computation│
│ • Info/frozen    │ │   (list pruning) │ │ • End-to-end     │
│   index split    │ │ • CA-SCL Decode  │ │   test           │
│ • Encoding       │ │   (CRC verify)   │ │ • BER            │
│   matrix (Kronecker)│ • f-function     │ │   computation    │
│ • CRC-16-CCITT   │ │   (box-plus)     │ │ • BPSK modulation│
│                  │ │ • g-function      │ │                  │
└──────────────────┘ │ • Bit-reversal   │ └──────────────────┘
                      │   ordering       │
                      └──────────────────┘
```

---

## 🔬 Decoding Algorithms | 解码算法

### 1. SC (Successive Cancellation) | 连续消除解码

The fundamental polar decoding algorithm. Decodes bits one-by-one in reliability order, using previously decoded bits as side information. Recursive implementation with f-function (box-plus) and g-function.

### 2. SCL (Successive Cancellation List) | 列表连续消除解码

Keeps a list of L most likely candidate paths at each step. At each bit position:
- Frozen bits: only one candidate (bit=0)
- Info bits: two candidates (bit=0 and bit=1), then prune to best L

This provides significant performance gain over SC at the cost of O(L·N·log N) complexity.

### 3. CA-SCL (CRC-Aided SCL) | CRC 辅助列表解码

Adds CRC bits to the information bits before encoding. After SCL decoding, selects the candidate path that passes CRC verification. This is the decoding scheme used in 5G NR and provides near-ML performance.

---

## 📊 Key Components | 核心组件

### f-function (Box-Plus) | f 函数（盒加运算）

```
f(a, b) = 2 · artanh(tanh(a/2) · tanh(b/2))
```

Computes the LLR of the XOR of two bits from their individual LLRs. Implemented with high-precision tanh approximation and numerical stability handling.

### g-function | g 函数

```
g(a, b, u) = (-1)^u · a + b
```

Computes the LLR of the right half given the left half decision.

### Encoding Matrix | 编码矩阵

```
G_N = F^⊗n  where F = [[1,0],[1,1]], n = log2(N)
```

Built via iterative Kronecker product.

---

## 🚀 Quick Start | 快速开始

### Installation | 安装

```bash
pip install numpy
```

### Basic Usage | 基本使用

```python
from polar_codes_fixed import PolarConfig, PolarSystem
import numpy as np

# Create polar code: N=16, K=8, GA design, SCL decoding with list size 8
config = PolarConfig(N=16, K=8, design='ga', design_snr_db=2.0,
                     use_crc=True, use_scl=True, list_size=8)
system = PolarSystem(config)

# Generate random info bits
info_bits = np.random.randint(0, 2, config.K, dtype=np.uint8)

# End-to-end test over AWGN channel at 10 dB SNR
success, decoded = system.end_to_end_test(info_bits, snr_db=10.0)
print(f"Original:  {info_bits}")
print(f"Decoded:   {decoded}")
print(f"Success:   {success}")
```

### BER Performance Test | 误码率测试

```python
# Compute BER at SNR=5 dB over 1000 trials
ber = system.compute_ber(num_trials=1000, snr_db=5.0)
print(f"BER (SNR=5dB): {ber:.6f}")
```

### Run Tests | 运行测试

```bash
# Quick test (N=8, K=4)
python polar_codes_fixed.py

# End-to-end verification
python tests/test_end_to_end.py

# BER reproduction
python tests/test_ber_reproduce.py

# Large code length test (N=128)
python tests/large_n_test_fixed.py
```

---

## 📁 Project Structure | 项目结构

```
Polar-Codes-SCSCL/
├── polar_codes_fixed.py          # Main implementation (28KB)
│   ├── PolarConfig                # Configuration class
│   ├── PolarEncoder               # Encoder (GA/PW ordering, CRC)
│   ├── PolarDecoder               # Decoder (SC, SCL, CA-SCL)
│   └── PolarSystem                # Complete system (channel, BER)
├── tests/
│   ├── test_end_to_end.py         # End-to-end encode/decode test
│   ├── test_ber_reproduce.py      # BER performance reproduction
│   ├── large_n_test_fixed.py      # Large code length (N=128) test
│   └── verify_basic_flow.py       # Basic flow verification
├── final_summary.md                # Bug fix summary (Chinese)
├── test_results.md                 # Test results documentation
└── README.md                       # This file
```

---

## 🔧 Configuration Options | 配置选项

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `N` | int | 8 | Code length (must be power of 2) |
| `K` | int | 4 | Number of information bits |
| `design` | str | 'ga' | Reliability ordering: 'ga', 'pw', 'de', 'custom' |
| `design_snr_db` | float | 1.0 | Design SNR for GA method (dB) |
| `use_crc` | bool | False | Enable CRC-16-CCITT |
| `crc_polynomial` | hex | 0x11021 | CRC polynomial |
| `use_scl` | bool | False | Use SCL instead of SC decoding |
| `list_size` | int | 8 | SCL list size L |

---

## 📈 Performance Notes | 性能说明

### Decoding Complexity | 解码复杂度

| Algorithm | Time Complexity | Space Complexity |
|-----------|----------------|-----------------|
| SC | O(N log N) | O(N) |
| SCL | O(L · N · log N) | O(L · N) |
| CA-SCL | O(L · N · log N) | O(L · N) |

### BER Performance | 误码率性能

- **SC**: Baseline performance, limited by error propagation
- **SCL (L=8)**: Significant improvement over SC, especially at moderate SNR
- **CA-SCL (L=8, CRC-16)**: Near-maximum-likelihood performance, used in 5G NR

### Bug Fixes | 修复内容

This implementation fixes several critical bugs found in common polar code implementations:
1. ✅ Recursive decoding merge order (frozen bit constraint violation)
2. ✅ f-function sign handling and numerical stability
3. ✅ BPSK symbol mapping (x=0→+1, x=1→-1)
4. ✅ LLR computation formula (4·SNR·y)
5. ✅ Encoding matrix construction (Kronecker product)
6. ✅ Info/frozen index assignment (non-overlapping, full coverage)

---

## 📚 References | 参考文献

1. **Arıkan, E.** (2009). *Channel polarization: A method for constructing capacity-achieving codes for symmetric binary-input memoryless channels.* IEEE Transactions on Information Theory, 55(7), 3051-3073.
2. **Tal, I., & Vardy, A.** (2015). *List decoding of polar codes.* IEEE Transactions on Information Theory, 61(5), 2213-2226.
3. **Niu, K., & Chen, K.** (2012). *CRC-aided decoding of polar codes.* IEEE Communications Letters, 16(10), 1668-1671.
4. **Trifonov, P.** (2012). *Efficient design and decoding of polar codes.* IEEE Transactions on Communications, 60(11), 3221-3227.
5. **3GPP TS 38.212** - 5G NR Multiplexing and channel coding specification.

---

## 📄 License | 许可证

MIT License — free to use, modify, and distribute.

---

<div align="center">

**Built with 📡 for 5G communications research**

[Report Bug](https://github.com/Windyhhh/Polar-Codes-SCSCL/issues) · [Request Feature](https://github.com/Windyhhh/Polar-Codes-SCSCL/issues)

</div>
