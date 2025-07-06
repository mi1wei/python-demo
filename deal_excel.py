# import pandas as pd
#
# # 读取 Excel 文件
# excel_file = pd.ExcelFile('task.xlsx')  # 替换为实际文件路径
#
# # 获取所有表名
# sheet_names = excel_file.sheet_names
# print(sheet_names)
#
# # 选择要读取的工作表（例如第一个工作表）
# df = excel_file.parse('信息表')  # 替换为实际表名
#
# # 查看数据基本信息
# print('数据基本信息：')
# df.info()
#
# # 查看数据集行数和列数
# rows, columns = df.shape
#
# if columns >= 5:
#     # 列数足够时获取第1、2、3列(index=0,1,2)
#     df_selected = df.iloc[:, [0, 1, 4,10]]
# else:
#     # 列数不足时获取全部列
#     df_selected = df.copy()
#
# # 查看结果
# print('数据全部内容信息：')
# df_selected.to_csv('output.csv',sep=',', na_rep='nan', index=False)
#
#
#


import pandas as pd


def merge_excel_columns(excel_path, sheet_config, output_txt_path):
    """
    从Excel文件的多个工作表中提取指定列，横向合并成一行，使用逗号分隔

    参数:
    excel_path: Excel文件路径
    sheet_config: 工作表配置字典，格式为 {工作表名称: [列索引1, 列索引2, ...]}
    output_txt_path: 输出TXT文件路径
    """
    try:
        # 读取Excel文件
        excel_file = pd.ExcelFile(excel_path)

        # 获取所有工作表中最大的行数
        max_rows = 0
        for sheet_name in sheet_config:
            df = excel_file.parse(sheet_name)
            max_rows = max(max_rows, len(df))

        # 用于存储所有行的数据
        all_lines = []

        # 处理每一行
        for row_idx in range(max_rows):
            row_data = []

            # 遍历每个工作表
            for sheet_name, column_indices in sheet_config.items():
                df = excel_file.parse(sheet_name)

                # 提取指定列
                if not column_indices:  # 如果没有指定列，则跳过该工作表
                    continue

                # 检查列索引是否有效
                valid_indices = [idx for idx in column_indices if idx < len(df.columns)]

                # 获取当前行的数据，如果行不存在则用空值填充
                if row_idx < len(df):
                    sheet_row = [str(df.iloc[row_idx, idx]) if idx < len(df.columns) else '' for idx in column_indices]
                else:
                    sheet_row = [''] * len(column_indices)

                # 添加到当前行的数据
                row_data.extend(sheet_row)

            # 将当前行的数据合并为一行，使用逗号分隔
            merged_line = ','.join(row_data)
            all_lines.append(merged_line)

        # 写入TXT文件，每行数据占一行
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_lines))

        print(f"数据合并成功，已保存到 {output_txt_path}")

    except Exception as e:
        print(f"处理过程中出错: {e}")


# 主程序
if __name__ == "__main__":
    # Excel文件路径
    excel_path = "task.xlsx"

    # 配置每个工作表要提取的列索引(从0开始)
    sheet_config = {
        "信息表": [0, 1, 2, 4, 10],  # 提取信息表的第1、2、3列
        "推特": [2, 3, 7],  # 提取推特表的第2、4、5列
        "Discord": [3, 4, 2]  # 提取discord表的第3、6、7列
    }

    # 输出TXT文件路径
    output_txt_path = "合并结果.txt"

    # 调用函数执行合并操作
    merge_excel_columns(excel_path, sheet_config, output_txt_path)
