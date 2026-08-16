"""
文档转换工具 - 统一入口
支持: PDF->Word, PPT->PDF, Word->PDF, DOC->DOCX
"""

import sys
import subprocess
from pathlib import Path


# 获取当前脚本所在目录
SCRIPT_DIR = Path(__file__).parent

# 定义转换脚本映射
CONVERTERS = {
    "1": {
        "name": "DOC 转 DOCX",
        "script": "doc_to_docx.py",
        "description": "将 .doc 文件转换为 .docx 格式"
    },
    "2": {
        "name": "PDF 转 Word",
        "script": "pdf_to_word.py",
        "description": "将 PDF 文件转换为 Word (.docx) 格式"
    },
    "3": {
        "name": "PPT 转 PDF",
        "script": "ppt_to_pdf.py",
        "description": "将 PPT (.ppt/.pptx) 文件转换为 PDF"
    },
    "4": {
        "name": "Word 转 PDF",
        "script": "word_to_pdf.py",
        "description": "将 Word (.doc/.docx) 文件转换为 PDF"
    },
}


def print_banner():
    """打印欢迎横幅"""
    print("=" * 60)
    print("  📄 文档转换工具 - 统一入口")
    print("=" * 60)
    print()


def print_menu():
    """打印功能菜单"""
    print("请选择要执行的转换功能：")
    print("-" * 60)
    for key, info in CONVERTERS.items():
        print(f"  [{key}] {info['name']}")
        print(f"      {info['description']}")
        print()
    print("  [0] 退出")
    print("-" * 60)


def run_converter(script_name: str):
    """运行指定的转换脚本"""
    script_path = SCRIPT_DIR / script_name
    
    if not script_path.exists():
        print(f"❌ 错误: 找不到脚本文件 {script_name}")
        print(f"   请确保 {script_name} 与当前文件在同一目录下")
        return False
    
    print(f"\n🚀 正在启动: {script_name}")
    print("-" * 60)
    
    try:
        # 使用 subprocess 运行脚本，保留交互式输入功能
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=SCRIPT_DIR,
            check=False
        )
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断操作")
        return False
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        return False


def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        # 支持直接指定脚本名或编号
        if arg in CONVERTERS:
            # 编号模式: converter.py 1
            script_name = CONVERTERS[arg]["script"]
            print(f"📌 执行: {CONVERTERS[arg]['name']}")
            run_converter(script_name)
            return
        elif arg in ["--help", "-h"]:
            print("用法:")
            print("  converter.py              # 交互式菜单模式")
            print("  converter.py [编号]       # 直接执行指定功能")
            print("  converter.py --list       # 列出所有功能")
            print()
            print("编号列表:")
            for key, info in CONVERTERS.items():
                print(f"  {key} - {info['name']}")
            return
        elif arg in ["--list", "-l"]:
            print("可用的转换功能:")
            for key, info in CONVERTERS.items():
                print(f"  [{key}] {info['name']}")
            return
        else:
            print(f"❌ 未知参数: {arg}")
            print("使用 converter.py --help 查看帮助")
            return
    
    # 交互式菜单模式
    while True:
        print_banner()
        print_menu()
        
        choice = input("\n请输入选项 (0-4): ").strip()
        
        if choice == "0":
            print("\n👋 再见！")
            break
        
        if choice in CONVERTERS:
            info = CONVERTERS[choice]
            print(f"\n📌 执行: {info['name']}")
            run_converter(info["script"])
            
            # 执行完成后等待用户按键
            input("\n按 Enter 键返回菜单...")
        else:
            print("❌ 无效选项，请重新输入")
            input("按 Enter 键继续...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已退出")
        sys.exit(0)
