import json

# 从竞争站点价格数组中获取最低价
def get_lowest_price(price_str):
    try:
        price_float = float(price_str)
        return price_float  # 只有一个价格直接返回
    except ValueError:
        # 使用 json.loads 将字符串转换为列表
        price_list = json.loads(price_str.replace("'", "\""))
        # 排序价格列表并返回最低的价格
        sorted_prices = sorted(price_list)
        if sorted_prices:  # 确保列表不为空
            return sorted_prices[0]  # 返回最低价格
        else:
            return None  # 如果列表为空，则返回None或其他适当的值

# 测试
price_str = '["19.99", "20.50", "21.75"]'
lowest_price = get_lowest_price(price_str)
print(lowest_price)  # 输出应该是 19.99

# 从竞争站点价格数组中获取次低价
def get_second_lowest_price(price_str):
    try:
        price_float = float(price_str)
        return price_float  # 只有一个价格直接返回
    except ValueError:
        # 使用 json.loads 将字符串转换为列表
        price_list = json.loads(price_str.replace("'", "\""))
        # 排序价格列表并返回第二低的价格
        sorted_prices = sorted(price_list)
        if len(sorted_prices) >= 2:
            return sorted_prices[1]  
        else:
            return sorted_prices[0]  
        # low_price = min(price_list)
        # return low_price
# 测试
# print(get_second_lowest_price("[5.84, 7.85, 8.25]"))
# print(get_second_lowest_price("8.25"))


# 从竞争站点价格数组，和自身价格中获取价差
def get_diff_price(price, other_price_list):
    other_price = get_second_lowest_price(other_price_list)     #获取其它站点的对比价格
    diff_price = round(price -other_price ,2)
    return diff_price   #返回值是我们的价格比对方高多少
# 测试
# price = 8.1
# other_price_list = "[5.84, 7.94, 8.25]"
# print(f"本站点油价：{price}")
# print(f"竞争站点油价：{other_price_list}")
# print(f"两者价差：{get_diff_price(price, other_price_list)}")


