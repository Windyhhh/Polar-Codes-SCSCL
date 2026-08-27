<div align="center">

# 📡 Polar-Codes-SCSCL

### 5G polar code SC/SCL/CA-SCL decoder implementations.

Complete SC, SCL and CA-SCL decoding for polar codes — N = 4~128, CRC-16, GA/PW reliability ordering.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)

</div>

---

**Polar-Codes-SCSCL** implements the polar code decoding algorithms used in 5G: successive cancellation (SC), successive cancellation list (SCL) and CRC-aided SCL (CA-SCL). It supports code lengths **N = 4~128**, **CRC-16**, and both **GA** and **PW** reliability ordering.

> [!NOTE]
> 中文项目：5G 极化码完整 SC/SCL/CA-SCL 译码实现，含 BER 复现与端到端测试。

---

## Quickstart

```bash
git clone https://github.com/Windyhhh/Polar-Codes-SCSCL.git
cd Polar-Codes-SCSCL

python polar_codes_fixed.py

# run the test suite
python tests/verify_basic_flow.py
python tests/test_end_to_end.py
python tests/test_ber_reproduce.py
python tests/large_n_test_fixed.py
```

---

## Features

- **SC / SCL / CA-SCL** — three decoding algorithms in one codebase.
- **Flexible parameters** — N = 4~128, CRC-16, GA/PW ordering.
- **Verified** — BER reproduction and end-to-end tests included.

---

## Project Structure

```
Polar-Codes-SCSCL/
├── polar_codes_fixed.py       # core decoder implementation
├── final_summary.md
├── test_results.md
└── tests/
    ├── verify_basic_flow.py
    ├── test_end_to_end.py
    ├── test_ber_reproduce.py
    └── large_n_test_fixed.py
```

---

## License

MIT — free to use, modify and distribute.
