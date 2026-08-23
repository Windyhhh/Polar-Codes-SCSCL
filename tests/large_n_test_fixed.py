#!/usr/bin/env python3
"""测试大码长（N=1024）的误码率 - 使用修复后的代码"""

import numpy as np
from polar_codes_fixed import PolarConfig, PolarSystem

def test_large_n_performance():
    """测试大码长（N=1024）的误码率"""
    print("=== 测试大码长（N=1024）的误码率 ===")
    
    # 测试配置
    N = 1024
    K = 512  # 码率0.5
    snr_values = [6.0, 8.0, 10.0]  # 测试的SNR值
    num_trials = 200  # 每个SNR点的试验次数，增加次数提高统计可靠性
    
    print(f"配置: N={N}, K={K}, 码率={K/N:.2f}")
    
    for snr_db in snr_values:
        print(f"\n--- SNR = {snr_db} dB ---")
        
        # 测试SC解码（GA设计）
        print(f"  测试SC解码（GA设计）...")
        config_sc_ga = PolarConfig(N=N, K=K, design='ga', design_snr_db=snr_db, use_scl=False)
        system_sc_ga = PolarSystem(config_sc_ga)
        ber_sc_ga = system_sc_ga.compute_ber(num_trials=num_trials, snr_db=snr_db)
        print(f"  SC解码（GA设计）BER: {ber_sc_ga:.6f}")
        
        # 测试SC解码（密度进化设计）
        print(f"  测试SC解码（密度进化设计）...")
        config_sc_de = PolarConfig(N=N, K=K, design='de', design_snr_db=snr_db, use_scl=False)
        system_sc_de = PolarSystem(config_sc_de)
        ber_sc_de = system_sc_de.compute_ber(num_trials=num_trials, snr_db=snr_db)
        print(f"  SC解码（密度进化设计）BER: {ber_sc_de:.6f}")
        
        # 使用密度进化设计的结果作为基准
        ber_sc = ber_sc_de
        
        # 测试不同列表大小的SCL解码
        for list_size in [4, 8, 16, 32, 64]:
            print(f"  测试SCL解码（列表大小={list_size}）...")
            config_scl = PolarConfig(N=N, K=K, design='ga', design_snr_db=snr_db, use_scl=True, list_size=list_size)
            system_scl = PolarSystem(config_scl)
            ber_scl = system_scl.compute_ber(num_trials=num_trials, snr_db=snr_db)
            print(f"  SCL解码（列表大小={list_size}）BER: {ber_scl:.6f}")
            
            # 计算提升倍数
            if ber_sc > 0:
                improvement = ber_sc / ber_scl
                print(f"  相对于SC解码的提升倍数: {improvement:.2f}x")
        
        # 测试CRC辅助的SCL解码（CA-SCL）
        print(f"  测试CRC辅助的SCL解码（CA-SCL，列表大小=8）...")
        config_ca_scl = PolarConfig(N=N, K=K, design='ga', design_snr_db=snr_db, use_scl=True, list_size=8, use_crc=True)
        system_ca_scl = PolarSystem(config_ca_scl)
        ber_ca_scl = system_ca_scl.compute_ber(num_trials=num_trials, snr_db=snr_db)
        print(f"  CA-SCL解码BER: {ber_ca_scl:.6f}")
        
        # 计算相对于SC解码的提升倍数
        if ber_sc > 0:
            improvement = ber_sc / ber_ca_scl
            print(f"  相对于SC解码的提升倍数: {improvement:.2f}x")
    
    print("\n=== 大码长测试完成 ===")

if __name__ == "__main__":
    test_large_n_performance()
