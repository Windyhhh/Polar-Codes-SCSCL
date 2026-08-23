#!/usr/bin/env python3
"""验证Polar码的基本编解码流程"""

import numpy as np
from polar_codes_fixed import PolarConfig, PolarSystem


def verify_basic_flow():
    """验证基本编解码流程"""
    print("=== 验证Polar码基本编解码流程 ===")
    
    # 使用小码长进行测试，更容易验证正确性
    config = PolarConfig(N=16, K=8, design='pw', use_scl=False)
    system = PolarSystem(config)
    
    print(f"码长 N={config.N}, 信息位长度 K={config.K}")
    print(f"信息位索引: {system.encoder.info_indices}")
    print(f"冻结位索引: {system.encoder.frozen_indices}")
    
    # 测试编码
    print("\n--- 测试编码 ---")
    info_bits = np.array([0, 1, 0, 1, 1, 0, 1, 0], dtype=np.uint8)
    print(f"输入信息位: {info_bits}")
    
    encoded = system.encoder.encode(info_bits)
    print(f"编码结果: {encoded}")
    
    # 测试信道模拟
    print("\n--- 测试信道模拟 ---")
    received = system.simulate_channel(encoded, snr_db=15.0)  # 高SNR确保正确判决
    print(f"接收信号: {received[:4]}...")
    
    # 测试LLR计算
    print("\n--- 测试LLR计算 ---")
    llr = system.llr_from_received(received, snr_db=15.0)
    print(f"LLR值: {llr[:4]}...")
    
    # 测试SC解码
    print("\n--- 测试SC解码 ---")
    decoded_sc = system.decoder.decode(llr, use_scl=False)
    print(f"SC解码结果: {decoded_sc}")
    print(f"解码是否正确: {'✅' if np.array_equal(info_bits, decoded_sc) else '❌'}")
    
    # 测试SCL解码
    print("\n--- 测试SCL解码 ---")
    decoded_scl = system.decoder.decode(llr, use_scl=True)
    print(f"SCL解码结果: {decoded_scl}")
    print(f"解码是否正确: {'✅' if np.array_equal(info_bits, decoded_scl) else '❌'}")
    
    # 测试端到端
    print("\n--- 测试端到端流程 ---")
    success, decoded = system.end_to_end_test(info_bits, snr_db=15.0)
    print(f"端到端测试结果: {'✅' if success else '❌'}")
    print(f"输入: {info_bits}")
    print(f"输出: {decoded}")
    
    return success


if __name__ == "__main__":
    verify_basic_flow()