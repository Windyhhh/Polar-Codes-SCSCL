import numpy as np
import torch
from models.models.vit_polar_system_fixed import ViT_Polar_System_Fixed
import time

# 重现之前的测试结果
def test_ber_reproduce():
    print("=== 重现之前的测试结果 ===")
    
    # 测试配置 - 与之前相同
    test_configs = [
        # (N, K, list_size, use_crc)
        (128, 64, 8, False),   # 禁用CRC，与之前相同
    ]
    
    # 噪声强度
    noise_levels = [0.0]
    
    # 测试图像数量
    num_images = 50
    image_size = 224
    
    # 生成测试图像和真实符号
    print("生成测试数据...")
    images = []
    true_symbols = []
    
    for i in range(num_images):
        # 生成随机灰度图像 - 与之前相同的形状
        image = torch.rand((1, image_size, image_size))  # 通道数=1，灰度图像
        images.append(image)
        
        # 生成随机符号（0-15）
        true_symbol = np.random.randint(0, 16)
        true_symbols.append(true_symbol)
    
    print(f"生成了 {num_images} 张测试图像")
    
    # 对每个配置进行测试
    for config in test_configs:
        N, K, list_size, use_crc = config
        print(f"\n--- 测试配置: N={N}, K={K}, list_size={list_size}, CRC={use_crc} ---")
        
        # 初始化系统
        system = ViT_Polar_System_Fixed(
            num_classes=16,
            polar_N=N,
            polar_K=K,
            use_scl=True,
            list_size=list_size,
            use_crc=use_crc
        )
        
        # 测试不同噪声强度
        for noise_std in noise_levels:
            print(f"\n  噪声强度: {noise_std}")
            
            start_time = time.time()
            
            # 评估误码率
            ber = system.evaluate_ber(images, true_symbols, noise_std=noise_std)
            
            elapsed_time = time.time() - start_time
            
            print(f"  误码率 (BER): {ber:.6f}")
            print(f"  测试时间: {elapsed_time:.2f} 秒")
            
            # 计算准确率
            accuracy = 1.0 if ber < 0.5 else 0.0
            print(f"  准确率: {accuracy:.2f}")
    
    print("\n=== 测试完成 ===")

# 运行测试
if __name__ == "__main__":
    test_ber_reproduce()
