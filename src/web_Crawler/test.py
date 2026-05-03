import json
import polars as pl

# ========== 读取JSON文件 ==========
def load_json_data(file_path):
    """读取JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# ========== 转换为Excel ==========
def json_to_excel(json_file_path, excel_file_path):
    """
    将题目JSON转换为Excel文件
    
    参数:
        json_file_path: JSON文件路径
        excel_file_path: 输出Excel文件路径
    """
    # 读取JSON数据
    data = load_json_data(json_file_path)
    
    # 转换为DataFrame
    df = pl.DataFrame(data)
    
    # 选择需要的列
    df = df.select(["序号", "题目", "填空题答案"])
    
    # 写入Excel
    df.write_excel(excel_file_path)
    
    print(f"转换完成！已保存到: {excel_file_path}")
    print(f"共 {len(df)} 条题目")

# ========== 主程序 ==========
if __name__ == "__main__":
    # 配置文件路径（请修改为实际路径）
    input_json = r"C:\Users\asus\Desktop\学校作业\通信原理\筛选后的题目-填空题-已爬取.json"
    output_excel = r"C:\Users\asus\Desktop\学校作业\通信原理\题目答案.xlsx"
    
    # 执行转换
    json_to_excel(input_json, output_excel)
    
    # 预览前几条数据
    data = load_json_data(input_json)
    print("\n预览前3条数据:")
    print("-" * 60)
    for item in data[:3]:
        print(f"序号: {item['序号']}")
        print(f"题目: {item['题目'][:50]}...")
        print(f"答案: {item['填空题答案']}")
        print("-" * 40)
