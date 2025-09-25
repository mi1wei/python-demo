import csv
import os


def get_value(row, index, default=""):
    """安全地从列表中获取值，超出范围时返回默认值"""
    return row[index] if len(row) > index else default


def load_csv(file_path):
    """读取 CSV 文件，返回行列表，忽略空行"""
    if not os.path.exists(file_path):
        print(f"警告: 文件未找到 -> {file_path}")
        return []
    with open(file_path, mode='r', encoding='utf-8') as file:
        return [row for row in csv.reader(file) if row]


def merge_column_data(rows, target, keys):
    """将 rows 数据按行号合并到 target 中，对应 keys"""
    for i, row in enumerate(rows):
        if i < len(target):
            for j, key in enumerate(keys):
                if j < len(row):
                    target[i][key] = row[j]
                else:
                    print(f"警告: 第{i + 1}行 {key} 缺失")


def get_browser_metadata(dir_path: str):
    browser_info = []

    # 读取主文件 okx（基础数据）
    okx_path = os.path.join(dir_path, "okx")
    okx_rows = load_csv(okx_path)
    for row in okx_rows:
        browser_info.append({
            'seq': int(get_value(row, 0, "0")),
            'browser_id': get_value(row, 1),
            'email': get_value(row, 2),
            'okx_ethers_private_key': get_value(row, 3),
            'okx_solana_private_key': get_value(row, 4),
            'x_username': get_value(row, 5),
            'x_password': get_value(row, 6),
            'x_2fa': get_value(row, 7),
            'discord_email': get_value(row, 8),
            'discord_email_password': get_value(row, 9),
            'discord_2fa': get_value(row, 10),
        })

    # 其他文件的字段合并逻辑（只需配置文件名和对应字段）
    merge_plan = [
        ("metamask", ["metamask_ethers_mnemonic"]),
        ("secondary_email", ["secondary_email"]),
        ("okx_eth_wallets", ["my_okx_eth_wallet_address", "my_okx_eth_wallet_private_key", "my_okx_eth_wallet_mnemonic"]),
        ("okx_solana_wallets",["my_okx_solana_wallet_address", "my_okx_solana_wallet_private_key", "my_okx_solana_wallet_mnemonic"]),
        ("metamask_eth_wallets",["my_metamask_solana_wallet_address", "my_metamask_solana_wallet_private_key", "my_metamask_solana_wallet_mnemonic"]),
        ("google", ["google_username","google_password"]),
        ("okx_solana_wallets_old", ["okx_solana_address", "okx_solana_private_key"]),
    ]

    for filename, keys in merge_plan:
        path = os.path.join(dir_path, filename)
        rows = load_csv(path)
        merge_column_data(rows, browser_info, keys)

    return browser_info


if __name__ == "__main__":
    print(get_browser_metadata('../configuration/primary'))
