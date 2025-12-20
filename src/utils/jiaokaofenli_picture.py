import time
import os
import pyautogui


class QuickBrowserAutomation:
    def __init__(self):
        # 创建截图保存目录
        self.screenshot_dir = "C:\\Users\\asus\\Desktop\\学校作业\\water"
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

        # 预设的按钮坐标（根据你刚才获取的坐标）
        self.save_btn_pos = (1439, 1187)  # 保存按钮
        self.analysis_btn_pos = (1298, 1189)  # 查看解析按钮
        self.next_btn_pos = (1384, 1185)  # 下一题按钮

        # 截图区域
        self.screenshot_region = (133, 302, 1394, 713)  # (x, y, width, height)

    def click_at_position(self, x, y):
        """在指定位置点击"""
        pyautogui.click(x, y)
        time.sleep(1)

    def take_screenshot(self, question_number):
        """截图并保存"""
        try:
            # 等待页面加载完成
            time.sleep(2)

            # 截图指定区域
            screenshot = pyautogui.screenshot(region=self.screenshot_region)
            filename = f"{self.screenshot_dir}/Q{question_number}.png"
            screenshot.save(filename)
            print(f"已保存截图: {filename}")

        except Exception as e:
            print(f"截图失败: {e}")

    def run_automation(self, total_questions, start_from=1):
        """运行自动化流程
        total_questions: 总题目数量
        start_from: 从第几题开始（用于断点续传）
        """
        print(f"开始自动化处理，从第{start_from}题到第{total_questions}题")

        current_question = start_from - 1  # 初始化当前题目编号

        try:
            for i in range(start_from, total_questions + 1):
                current_question = i  # 更新当前处理的题目
                print(f"\n正在处理第{i}题...")

                # 执行操作序列
                self.click_at_position(*self.save_btn_pos)
                self.click_at_position(*self.analysis_btn_pos)
                self.take_screenshot(i)
                self.click_at_position(*self.next_btn_pos)

                # 添加延迟避免操作过快
                time.sleep(1)

            print(f"\n自动化处理完成！共处理{total_questions - start_from + 1}题")

        except KeyboardInterrupt:
            print(f"\n用户中断操作，已处理到第{current_question}题")

    def show_settings(self):
        """显示当前设置"""
        print("\n当前配置:")
        print(f"保存按钮位置: {self.save_btn_pos}")
        print(f"查看解析按钮位置: {self.analysis_btn_pos}")
        print(f"下一题按钮位置: {self.next_btn_pos}")
        print(f"截图区域: {self.screenshot_region}")


def main():
    automation = QuickBrowserAutomation()

    # 显示当前配置
    automation.show_settings()

    try:
        total_questions = int(input("\n请输入总题目数量: "))
        start_from = int(input("从第几题开始? (默认从1开始): ") or 1)

        # 确认开始
        confirm = input(
            f"即将从第{start_from}题处理到第{total_questions}题，确认开始？(y/n): "
        ).lower()
        if confirm == "y" or confirm == "":
            print("\n请确保浏览器已打开并在目标页面")
            print("程序将在5秒后开始，请切换到浏览器窗口...")
            for i in range(5, 0, -1):
                print(f"{i}...")
                time.sleep(1)
            print("开始执行！")
            automation.run_automation(total_questions, start_from)
        else:
            print("操作已取消")

    except ValueError:
        print("请输入有效的数字！")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
