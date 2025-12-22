import polars as pl
import re


class SchoolExamDataProcess:
    def data_process(
        self,
        input_file: str,
        output_file: str,
        judge_column: str,
        keep_row: list[str],
        keep_column: list[str],
        pattern: str,
    ) -> None:
        """
        关于这个方法:  是用来整理学校发的excel表中的数据, 并进行清洗,
        可以根据需求决定是否需要转换成: word, 或者进一步转换成: PDF,
        后面会有对应的提示.
        :param input_file: 可以选择文件夹, 单文件, 多文件.
        :param output_file: 只能是文件夹.
        :param judge_column: 根据这一列来判断行是不是需要保留.
        :param keep_row: 存放你想要保留的行
        :param keep_column: 需要保留的列.
        :param pattern: 正则表达式的匹配(可选, 但是我估计一般是用不上)
        :return: None
        """

        # 正则表达式的编译(速度)优化
        # good_pattern = re.compile(pattern)

        df = pl.read_excel(input_file)
        # keep_column = ["题干", "正确答案", "选项A", "选项B", "选项C", "选项D"]
        # keep_row = ["单选题", "多选题", "判断题", "应用题"]

        ans = df.filter((pl.col(judge_column).is_in(keep_row))).select(
            pl.col(keep_column)
        )
        ans.write_excel(output_file)
