import polars as pl
from datetime import datetime
from loguru import logger as log
from pkuseg import pkuseg


# 计时装饰器
def timer(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        log.info(f"{func.__name__} 耗时: {end - start}")
        return result

    return wrapper


@timer
def extract_and_process(csv_file: str) -> pl.DataFrame:
    """
    从CSV文件中提取匹配项并进行处理
    """
    # 读取数据
    df = pl.read_csv(csv_file)

    # 正则模式
    pattern = r"\[\[\[([\u4E00-\u9FA5]{2}不堪)\]\]\]"

    # 提取和统计匹配项
    result = (
        df.select(
            pl.col("语料数据")
            .str.extract_all(pattern)
            .alias("匹配项")
        )
        .explode("匹配项")
        .filter(pl.col("匹配项").is_not_null())
        .group_by("匹配项")
        .agg(pl.col("匹配项").count().alias("出现次数"))
        .sort("出现次数", descending=True)
    )

    return result


@timer
def process_words(result_df: pl.DataFrame) -> pl.DataFrame:
    """
    处理匹配项，过滤并分词
    """
    # 获取匹配项列表
    ans_list = result_df.get_column("匹配项").to_list()

    # 创建分词器
    seg = pkuseg()

    # 使用列表推导式和条件判断一次性处理
    true_ans = [
        word for word in ans_list
        if len(seg.cut(word)) == 1
    ]

    log.info(f"符合条件的词语数量: {len(true_ans)}")

    # 创建DataFrame
    result_df = pl.DataFrame({"词语": true_ans})

    return result_df


def main():
    # 文件路径
    csv_file = r"F:\备份\2_姐姐给我的词频统计代码用于学习\副本语料（1）.csv"

    # 第一步：提取和处理匹配项
    result = extract_and_process(csv_file)

    print(result)

    # 第二步：进一步处理词语
    final_result = process_words(result)

    # 输出结果
    print("最终结果:")
    print(final_result)

    # 如果需要，可以保存到文件
    # final_result.write_csv("processed_words.csv")

    return final_result


if __name__ == "__main__":
    result = main()