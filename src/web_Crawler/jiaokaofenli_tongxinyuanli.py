import requests
from fake_useragent import UserAgent
import polars as pl
import re
import time

# ========== 1. 初始化会话 ==========
session = requests.Session()
session.headers.update({
    "User-Agent": UserAgent().random,
    "Cookie": "Hm_lvt_5a2a966e966e16256f6b2a11625b597b=1777699626,1777732546,1777777476; HMACCOUNT=2A0B3DB91DEC60CD; Admin-Token=eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjY5ZDhjYzg5LTQ4ZjAtNGMwNy05ZDc3LTE1N2RjN2MxNWIxZiJ9.-Po4-AJRkrL23Bdewrrwo1XQh1krmeGlD-6LA6d_KY_xX-gR0tL9mlA0nDiPHKFUx-dzD6OMHCoMbhDdgJ8Jcg; Hm_lpvt_5a2a966e966e16256f6b2a11625b597b=1777779433",
    "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjY5ZDhjYzg5LTQ4ZjAtNGMwNy05ZDc3LTE1N2RjN2MxNWIxZiJ9.-Po4-AJRkrL23Bdewrrwo1XQh1krmeGlD-6LA6d_KY_xX-gR0tL9mlA0nDiPHKFUx-dzD6OMHCoMbhDdgJ8Jcg",
    "Referer": "https://wisdom2.prod.shangyuninfo.com/class/details/special?roomId=2049080533266354177",
})

# ========== 2. 定义数据清洗函数 ==========
def clean_html(text):
    """去除 HTML 标签"""
    if text:
        return re.sub(r"<[^>]+>", "", text)
    return ""

def fetch_question(card_order):
    """获取指定序号的题目"""
    target_url = f"https://wisdom2.prod.shangyuninfo.com/prod-api/roomUserQuestion/info/question?cardOrder={card_order}"
    
    try:
        response = session.get(url=target_url)
        response.encoding = "utf-8"
        response.raise_for_status()
        
        json_data = response.json()
        
        # 检查是否成功获取数据
        if json_data.get("code") == 200 and json_data.get("data"):
            data = json_data["data"]
            return {
                "序号": card_order,
                "题目": data.get("subjectMatterTxt", ""),
                "选项A": clean_html(data.get("optionA", "")),
                "选项B": clean_html(data.get("optionB", "")),
                "选项C": clean_html(data.get("optionC", "")),
                "选项D": clean_html(data.get("optionD", "")),
                "答案": data.get("answer", ""),
            }
        else:
            print(f"序号 {card_order}: 无数据或接口返回错误 - {json_data.get('msg', '未知错误')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"序号 {card_order}: 请求失败 - {e}")
        return None
    except ValueError as e:
        print(f"序号 {card_order}: JSON 解析失败 - {e}")
        return None

# ========== 3. 批量爬取题目 ==========
def crawl_questions(start=1, end=176, delay=0.5):
    """
    批量爬取题目
    
    参数:
        start: 起始序号
        end: 结束序号
        delay: 请求间隔（秒），避免请求过快
    """
    all_questions = []
    
    print(f"开始爬取题目，范围: {start} - {end}")
    print("-" * 50)
    
    for i in range(start, end + 1):
        print(f"正在爬取第 {i}/{end} 题...", end=" ")
        
        question_data = fetch_question(i)
        
        if question_data:
            all_questions.append(question_data)
            print("✓ 成功")
        else:
            print("✗ 失败")
        
        # 添加延迟，避免请求过快
        if i < end:
            time.sleep(delay)
    
    print("-" * 50)
    print(f"爬取完成！成功: {len(all_questions)} 题，失败: {end - start + 1 - len(all_questions)} 题")
    
    return all_questions

# ========== 4. 保存数据到文件 ==========
def save_to_excel(data, filepath):
    """保存到 Excel 文件（需要安装 xlsxwriter）"""
    if not data:
        print("没有数据可保存")
        return
    
    df = pl.DataFrame(data)
    df.write_excel(filepath)
    print(f"已保存到 Excel: {filepath}")
    return df

def save_to_json(data, filepath):
    """保存到 JSON 文件"""
    if not data:
        print("没有数据可保存")
        return
    
    import json
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已保存到 JSON: {filepath}")

# ========== 5. 主程序 ==========
def main():
    # 配置参数
    START = 1      # 起始序号
    END = 2       # 结束序号（先测试10题，确认没问题再改回176）
    DELAY = 0.5    # 请求间隔（秒）
    
    # 输出文件路径
    excel_output = r"C:\Users\asus\Desktop\学校作业\kaishi\题目数据.xlsx"
    json_output = r"C:\Users\asus\Desktop\学校作业\kaishi\题目数据.json"
    
    # 1. 爬取题目
    questions = crawl_questions(START, END, DELAY)
    
    if not questions:
        print("没有获取到任何题目数据！")
        return
    
    # 2. 保存到不同格式
    save_to_excel(questions, excel_output)
    save_to_json(questions, json_output)
       
    # 4. 显示统计信息
    print("\n统计信息:")
    print(f"总题目数: {len(questions)}")
    
# ========== 6. 断点续传功能（可选） ==========
def resume_crawl(existing_file, start, end):
    """
    断点续传：从已有文件继续爬取
    
    参数:
        existing_file: 已存在的 CSV 文件路径
        start: 开始序号
        end: 结束序号
    """
    # 读取已爬取的序号
    df_existing = pl.read_csv(existing_file)
    existing_numbers = set(df_existing["序号"].to_list())
    
    # 找出缺失的序号
    all_numbers = set(range(start, end + 1))
    missing_numbers = sorted(all_numbers - existing_numbers)
    
    print(f"已存在 {len(existing_numbers)} 题，缺失 {len(missing_numbers)} 题")
    print(f"缺失序号: {missing_numbers[:20]}..." if len(missing_numbers) > 20 else f"缺失序号: {missing_numbers}")
    
    # 爬取缺失的题目
    new_questions = []
    for num in missing_numbers:
        question_data = fetch_question(num)
        if question_data:
            new_questions.append(question_data)
        time.sleep(1.5)
    
    # 合并并保存
    if new_questions:
        df_new = pl.DataFrame(new_questions)
        df_combined = pl.concat([df_existing, df_new])
        df_combined.write_csv(existing_file)
        print(f"续传完成！新增 {len(new_questions)} 题")
    
    return df_combined if new_questions else df_existing

if __name__ == "__main__":
    main()
