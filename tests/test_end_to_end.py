import numpy as np
import torch
from models.models.vit_polar_system_fixed import ViT_Polar_System_Fixed

# 验证整个系统的端到端功能
def test_end_to_end():
    print("=== 验证系统端到端功能 ===")
    
    # 初始化系统
    system = ViT_Polar_System_Fixed(
        num_classes=16,
        polar_N=64,
        polar_K=32,
        use_scl=True,
        list_size=8,
        use_crc=False
    )
    
    # 生成测试图像（灰度图像）
    image_size = 224
    image = torch.rand((1, 1, image_size, image_size))  # 批次大小=1，通道数=1，灰度图像
    
    print("\n--- 测试分类模式 ---")
    # 测试分类模式
    class_logits, confidence_scores = system.forward(image, mode='classification')
    print(f"分类logits形状: {class_logits.shape}")
    print(f"置信度分数形状: {confidence_scores.shape}")
    
    # 计算预测类别
    probabilities = torch.softmax(class_logits, dim=1)
    predicted_class = torch.argmax(probabilities, dim=1).item()
    print(f"预测类别: {predicted_class}")
    print(f"预测概率: {probabilities[0, predicted_class].item():.4f}")
    
    print("\n--- 测试端到端解码模式 ---")
    # 测试端到端解码模式
    decoded_bits, class_logits, symbol_probs = system.forward(image, mode='e2e')
    print(f"解码比特形状: {decoded_bits.shape}")
    print(f"分类logits形状: {class_logits.shape}")
    print(f"符号概率形状: {symbol_probs.shape}")
    
    # 打印解码结果
    decoded_bits_np = decoded_bits.squeeze().cpu().numpy()
    print(f"解码比特前10位: {decoded_bits_np[:10]}")
    
    print("\n--- 测试无噪声解码 ---")
    # 测试无噪声解码
    info_bits = np.random.randint(0, 2, 32, dtype=np.uint8)
    decoded, success = system.test_noiseless_decode(info_bits)
    print(f"无噪声解码测试: {'✅ 成功' if success else '❌ 失败'}")
    print(f"输入前10位: {info_bits[:10]}")
    print(f"输出前10位: {decoded[:10]}")
    
    print("\n--- 测试符号到比特转换 ---")
    # 测试符号到比特转换
    for symbol in [0, 5, 10, 15]:
        bits = system.symbol_to_bits(symbol)
        print(f"符号 {symbol} -> 比特 {bits}")
    
    print("\n--- 测试比特到符号转换 ---")
    # 测试比特到符号转换
    test_bits = [0, 1, 0, 1]
    symbol = system.bits_to_symbol(test_bits)
    print(f"比特 {test_bits} -> 符号 {symbol}")
    
    print("\n=== 端到端功能验证完成 ===")

# 运行测试
if __name__ == "__main__":
    test_end_to_end()
