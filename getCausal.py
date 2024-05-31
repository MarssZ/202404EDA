from flask import Flask, jsonify, request

app = Flask(__name__)



# 超参数
COLS_ALL = ['date', 'amount', 'refuelLiters', 'order_cnt', 'text_day', 'text_night', 'high', 'low', 'wc_day', 'wd_day', 'wc_night', 'wd_night', 'week', 'holidays', 'encoded_wc_night', 'code_week', 'encoded_holidays', '305_price','305_order_cnt','305_amount','313_price','encode_label_305price','encode_weight_305price','313_order_cnt','313_amount' ]

import pandas as pd
import json

# 读取excel文件并获取指定列
df = pd.read_csv('Data\结果1_全站按日期分组_2023全年.csv', usecols=COLS_ALL, encoding='GBK')
# 将DataFrame转换为字典
data = df.to_dict(orient='records')

# 获取所有数据
@app.route('/date', methods=['GET'])
def get_todos():
    return jsonify(data)

def get_temperature_by_date(dataframe, specific_date):
    # 将字符串形式的日期转换为 datetime 类型
    specific_date = pd.to_datetime(specific_date)
    
    # 确保日期列类型为 datetime，这样可以避免比较错误
    if dataframe['date'].dtype != 'datetime64[ns]':
        dataframe['date'] = pd.to_datetime(dataframe['date'])
    
    # 获取 specific_date 对应的 high 列数值
    try:
        high_value = dataframe.query("date == @specific_date")['high']
        
        if high_value.empty:
            print(f"未找到日期为 {specific_date.strftime('%Y-%m-%d')} 的记录")
            return None
        else:
            return high_value.iloc[0]
    except KeyError as e:
        print(f"数据框中没有名为 'high' 的列: {e}")
        return None
        print(f"数据框中没有名为 'high' 的列: {e}")
        return None, None

def get_average_amount_by_holiday(dataframe, holiday):
    """
    获取指定节假日下的平均销售量

    参数:
    dataframe (pd.DataFrame): 数据框，其中 holidays 列表示节假日名称，amount 列表示销售量
    holiday (str): 要查询的节假日名称

    返回:
    float: 指定节假日对应的平均销售量，如果没有匹配的记录，则返回 None
    """
    
    # 检查数据框中是否包含必须的列
    if 'holidays' not in dataframe.columns or 'amount' not in dataframe.columns:
        print(f"数据框中没有名为 'holidays' 或 'amount' 的列")
        return None
    
    # 过滤并计算指定节假日的平均销售量
    holiday_df = dataframe[dataframe['holidays'] == holiday]
    
    if holiday_df.empty:
        print(f"未找到节假日为 '{holiday}' 的记录")
        return None
    
    average_amount = holiday_df['amount'].mean()
    return average_amount

def get_average_amount_by_weekday(dataframe, weekday):
    """
    获取指定温度下的平均销售量

    参数:
    dataframe (pd.DataFrame): 数据框，其中 week 列表示星期几，amount 列表示销量
    weekday (str): 要查询的星期值

    返回:
    float: 指定星期几下的平均销量，如果没有匹配的记录，则返回 None
    """
    
    # 确保 high 列和 amount 列存在于数据框中
    if 'week' not in dataframe.columns or 'amount' not in dataframe.columns:
        print("数据框中需要包含 'week' 和 'amount' 列")
        return None

    # 获取指定温度下的销量
    try:
        sales = dataframe.query("week == @weekday")['amount']
        
        if sales.empty:
            print(f"未找到week为 {weekday} 的记录")
            return None
        else:
            average_sales = sales.mean()
            return average_sales
    except KeyError as e:
        print(f"数据框中没有名为 '未找到week为' 或 'amount' 的列: {e}")
        return None
    
def get_average_amount_by_temperature(dataframe, temperature):
    """
    获取指定温度下的平均销售量

    参数:
    dataframe (pd.DataFrame): 数据框，其中 high 列表示温度，amount 列表示销量
    temperature (int or float): 要查询的温度值

    返回:
    float: 指定温度下的平均销量，如果没有匹配的记录，则返回 None
    """
    
    # 确保 high 列和 amount 列存在于数据框中
    if 'high' not in dataframe.columns or 'amount' not in dataframe.columns:
        print("数据框中需要包含 'high' 和 'amount' 列")
        return None

    # 获取指定温度下的销量
    try:
        sales = dataframe.query("high == @temperature")['amount']
        
        if sales.empty:
            print(f"未找到温度为 {temperature} 的记录")
            return None
        else:
            average_sales = sales.mean()
            return average_sales
    except KeyError as e:
        print(f"数据框中没有名为 'high' 或 'amount' 的列: {e}")
        return None
    
def get_average_amount_by_wc_night(dataframe, wc_night):
    """
    获取指定wc_night下的平均销售量

    参数:
    dataframe (pd.DataFrame): 数据框，其中 wc_night 列表示昨晚风力，amount 列表示销量
    wc_night (str): 要查询的wc_night昨晚风力

    返回:
    float: 指定wc_night风力下的平均销量，如果没有匹配的记录，则返回 None
    """
    
    # 确保 high 列和 amount 列存在于数据框中
    if 'wc_night' not in dataframe.columns or 'amount' not in dataframe.columns:
        print("数据框中需要包含 'wc_night' 和 'amount' 列")
        return None
    
    # 获取指定温度下的销量
    try:
        # 若风力为低风力状态，统一视为同一档(放弃)
        # if wc_night in ["<3级", "3~4级", "4~5级"]:
        #     wc_night = '<3级'

        sales = dataframe.query("wc_night == @wc_night")['amount']
        
        if sales.empty:
            print(f"未找到昨晚风力为 {wc_night} 的记录")
            return None
        else:
            average_sales = sales.mean()
            return average_sales
    except KeyError as e:
        print(f"数据框中没有名为 'wc_night' 或 'amount' 的列: {e}")
        return None

def get_predict_amount_by_encoded_305price(price305):
    """
    用调价指数来预估销量

    参数:
    dataframe (pd.DataFrame): 数据框，其中 wc_night 列表示昨晚风力，amount 列表示销量
    price305 (float): 调价指数

    返回:
    float: 指定encoded_305price下的预估销量，如果没有匹配的记录，则返回 None
    """
    #以下是基于2023年数据，线性回归得到的参数。未来要基于dataframe计算，这边考虑到性能问题，就不每次计算了。
    slope=-26708137.122280724
    intercept=374192453.93235
    y = slope * price305 + intercept
    return y 

def get_amount_by_date(dataframe, specific_date):
    """
    获取指定日期的销量

    参数:
    dataframe (pd.DataFrame): 数据框，其中 date 列表示日期，amount 列表示销量
    specific_date (str): 要查询的日期，格式为 'YYYY-MM-DD'

    返回:
    float: 指定日期的销量，如果没有匹配的记录，则返回 None
    """

    # 将字符串形式的日期转换为 datetime 类型
    specific_date = pd.to_datetime(specific_date)
    
    # 确保日期列类型为 datetime，这样可以避免比较错误
    if dataframe['date'].dtype != 'datetime64[ns]':
        dataframe['date'] = pd.to_datetime(dataframe['date'])
    
    # 获取 specific_date 对应的 amount 列数值
    try:
        amount_value = dataframe.query("date == @specific_date")['amount']
        
        if amount_value.empty:
            print(f"未找到日期为 {specific_date.strftime('%Y-%m-%d')} 的记录")
            return None
        else:
            return amount_value.iloc[0]
    except KeyError as e:
        print(f"数据框中没有名为 'amount' 的列: {e}")
        return None
    
def get_weekday_by_date(dataframe, specific_date):
    """
    获取指定日期所在的星期几

    参数:
    dataframe (pd.DataFrame): 数据框，其中 date 列表示日期
    specific_date (str): 要查询的日期，格式为 'YYYY-MM-DD'

    返回:
    int: 指定日期对应的星期几，如果没有匹配的记录，则返回 None
    """

    # 将字符串形式的日期转换为 datetime 类型
    specific_date = pd.to_datetime(specific_date)
    
    # 确保日期列类型为 datetime，这样可以避免比较错误
    if dataframe['date'].dtype != 'datetime64[ns]':
        dataframe['date'] = pd.to_datetime(dataframe['date'])
    
    # 获取 specific_date 对应的周数
    try:
        week_number = dataframe.query("date == @specific_date")['week']
        
        if week_number.empty:
            print(f"未找到日期为 {specific_date.strftime('%Y-%m-%d')} 的记录")
            return None
        else:
            return week_number.iloc[0]
    except KeyError as e:
        print(f"数据框中没有名为 'date' 的列: {e}")
        return None

def get_holidays_by_date(dataframe, specific_date):
    """
    获取指定日期所在的节假日字符串

    参数:
    dataframe (pd.DataFrame): 数据框，其中 date 列表示日期，holiday 列表示节假日
    specific_date (str): 要查询的日期，格式为 'YYYY-MM-DD'

    返回:
    str: 指定日期对应的节假日字符串，如果没有匹配的记录，则返回 None
    """

    # 将字符串形式的日期转换为 datetime 类型
    specific_date = pd.to_datetime(specific_date)
    
    # 确保日期列类型为 datetime，这样可以避免比较错误
    if dataframe['date'].dtype != 'datetime64[ns]':
        dataframe['date'] = pd.to_datetime(dataframe['date'])
    
    # 获取 specific_date 对应的节假日字符串
    try:
        holiday_info = dataframe.query("date == @specific_date")['holidays']
        
        if holiday_info.empty:
            print(f"未找到日期为 {specific_date.strftime('%Y-%m-%d')} 的记录")
            return None
        else:
            return holiday_info.iloc[0] if holiday_info.iloc[0] else "无节假日"
    except KeyError as e:
        print(f"数据框中没有名为 'holidays' 或 'date' 的列: {e}")
        return None

def get_wc_night_by_date(dataframe, specific_date):
    """
    获取指定日期所在的昨晚风力字符串

    参数:
    dataframe (pd.DataFrame): 数据框，其中 date 列表示日期
    specific_date (str): 要查询的日期，格式为 'YYYY-MM-DD'

    返回:
    str: 指定日期对应的昨晚风力字符串，如果没有匹配的记录，则返回 None
    """

    # 将字符串形式的日期转换为 datetime 类型
    specific_date = pd.to_datetime(specific_date)
    
    # 确保日期列类型为 datetime，这样可以避免比较错误
    if dataframe['date'].dtype != 'datetime64[ns]':
        dataframe['date'] = pd.to_datetime(dataframe['date'])
    
    # 获取 specific_date 对应的昨晚风力字符串
    try:
        wc_night_info = dataframe.query("date == @specific_date")['wc_night']
        
        if wc_night_info.empty:
            print(f"未找到日期为 {specific_date.strftime('%Y-%m-%d')} 的记录")
            return None
        else:
            return wc_night_info.iloc[0] if wc_night_info.iloc[0] else "无昨晚风力数据"
    except KeyError as e:
        print(f"数据框中没有名为 'wc_night' 或 'date' 的列: {e}")
        return None

def get_weight_305pricee_by_date(dataframe, specific_date):
    """
    获取指定日期所在的调价编码权重（这是一个精心设计的调价编码方式）

    参数:
    dataframe (pd.DataFrame): 数据框，其中 date 列表示日期
    specific_date (str): 要查询的日期，格式为 'YYYY-MM-DD'

    返回:
    str: 指定日期对应的调价编码，如果没有匹配的记录，则返回 None
    """

    # 将字符串形式的日期转换为 datetime 类型
    specific_date = pd.to_datetime(specific_date)
    
    # 确保日期列类型为 datetime，这样可以避免比较错误
    if dataframe['date'].dtype != 'datetime64[ns]':
        dataframe['date'] = pd.to_datetime(dataframe['date'])
    
    # 获取 specific_date 对应的调价编码数据
    try:
        encode_weight_305price_info = dataframe.query("date == @specific_date")['encode_weight_305price']
        
        if encode_weight_305price_info.empty:
            print(f"未找到日期为 {specific_date.strftime('%Y-%m-%d')} 的记录")
            return None
        else:
            return encode_weight_305price_info.iloc[0] if encode_weight_305price_info.iloc[0] else 0
    except KeyError as e:
        print(f"数据框中没有名为 'encode_weight_305price_info' 或 'date' 的列: {e}")
        return None

def get_label_305pricee_by_date(dataframe, specific_date):
    """
    获取指定日期所在的调价编码类别

    参数:
    dataframe (pd.DataFrame): 数据框，其中 date 列表示日期
    specific_date (str): 要查询的日期，格式为 'YYYY-MM-DD'

    返回:
    str: 指定日期对应的调价编码类别，如果没有匹配的记录，则返回 None
    """

    # 将字符串形式的日期转换为 datetime 类型
    specific_date = pd.to_datetime(specific_date)
    
    # 确保日期列类型为 datetime，这样可以避免比较错误
    if dataframe['date'].dtype != 'datetime64[ns]':
        dataframe['date'] = pd.to_datetime(dataframe['date'])
    
    # 获取 specific_date 对应的调价编码数据
    try:
        encode_label_305price_info = dataframe.query("date == @specific_date")['encode_label_305price']
        
        if encode_label_305price_info.empty:
            print(f"未找到日期为 {specific_date.strftime('%Y-%m-%d')} 的记录")
            return None
        else:
            return encode_label_305price_info.iloc[0] if encode_label_305price_info.iloc[0] else 0
    except KeyError as e:
        print(f"数据框中没有名为 'encode_label_305price_info' 或 'date' 的列: {e}")
        return None
def calculate_infra(array):
    """
    计算影响力权重
    
    参数:
    array (dict): 一个字典，其中键是影响因素的名称，值是其平均销量。
    
    返回:
    dict: 一个字典，其中键是影响因素的名称，值是其由其平均销量计算得到的影响权重。正面影响的权重为正值，负面影响的权重为负值。
    """
     # 对字典进行排序
    array = dict(sorted(array.items(), key=lambda item: item[1]))
    #print("排序后的数组:", array)

    ## 计算影响力权重
    positive_sum = 0 #正面影响
    negative_sum = 0 #负面影响
    all_sum = 0 #总计影响

    # 遍历字典，计算正负值的总和
    for value in array.values():
        all_sum +=value
        if value > 0:
            positive_sum += value
        elif value < 0:
            negative_sum += value
    print()
    print(f'positive_sum: {positive_sum:.2f}, negative_sum: {negative_sum:.2f}, all_sum: {all_sum:.2f} ')

    # 再次遍历字典，计算权重
    for key in array:
        if array[key] > 0:
            array[key] = array[key] / positive_sum 
        elif array[key] < 0:
            array[key] = - array[key] / negative_sum 
    # print("###计算归因影响因子:", array)
    return array

def analyze_infra(dataframe, date_y, date_x, array):
    """
    分析销量变化的归因因素，去除不必要的归因项， 并返回更新后的归因字典。

    参数:
    dataframe (pd.DataFrame): 包含销量数据的数据框。
    date_y (str): 对比的第一个日期，格式应为 "YYYY-MM-DD"。
    date_x (str): 对比的第二个日期，格式应为 "YYYY-MM-DD"。
    array (dict): 包含影响因素及其权重的字典，其中键是影响因素名称，值是其对应的权重。

    返回:
    dict: 更新后的归因字典，其中包含销量变化的描述和归因分析结果。字典的键是影响因素名称，值是描述影响权重的字符串。并增加汇总项。
    """
    keys_to_delete = []

    # 获取两个日期的销量数据，并计算变化量
    amount_y = get_amount_by_date(dataframe, date_y) / 10000
    amount_x = get_amount_by_date(dataframe, date_x) / 10000
    amount_resi = amount_y - amount_x

    # 根据销量变化量进行归因分析
    if amount_resi > 0:  # 销量增长归因
        amount_str = f'{date_y}和{date_x}相比，前者销量{amount_y:.2f}万，后者销量{amount_x:.2f}万。销量多了{amount_resi:.2f}万。'
        array = dict(sorted(array.items(), key=lambda item: item[1], reverse=True))  # 倒序重排
        for key in array:
            if array[key] < 0.001:  # 忽略过小的因素
                keys_to_delete.append(key)
    elif amount_resi < 0:  # 销量减少归因
        amount_str = f'{date_y}和{date_x}相比，前者销量{amount_y:.2f}万，后者销量{amount_x:.2f}万。销量少了{-amount_resi:.2f}万。'
        for key in array:
            if array[key] > -0.001:
                keys_to_delete.append(key)
    else:  # 销量无变化
        amount_str = f'{date_y}和{date_x}相比，前者销量{amount_y:.2f}万，后者销量{amount_x:.2f}万。销量无明显变化。'
        for key in array:
            keys_to_delete.append(key)

    # 删掉反方向的原因
    for key in keys_to_delete:
        del array[key]
    
    # 更新影响权重字典
    for key in array:
        if array[key] < 0:
            array[key] = -array[key]
        array[key] = f"影响权重{(array[key] * 100):.2f}%"

    # 打印归因分析结果
    print()
    array[amount_str] = '归因成功'
    print("归因分析:", json.dumps(array, indent=4, ensure_ascii=False))
    
    return array
    

## 单日对比归因
def compare_by_date(dataframe, date_y, date_x):
    # 温度归因
    temperature_y = get_temperature_by_date(dataframe,date_y)
    temperature_x = get_temperature_by_date(dataframe,date_x)
    temperature_str = f'{date_y}和{date_x}相比，前者最高温度为{temperature_y}而后者为{temperature_x}。从整体趋势上来看温度过高和过低销量都会更好，而适宜温度可能相对销量会低。'
    print(temperature_str)

    amount_y = get_average_amount_by_temperature(dataframe, temperature_y)
    amount_x = get_average_amount_by_temperature(dataframe, temperature_x)
    temperature_amount_resi = amount_y-amount_x
    print('温度因素差值amount_resi :'+ str(temperature_amount_resi))

    # weekday星期几归因
    weekday_y = get_weekday_by_date(dataframe,date_y)
    weekday_x = get_weekday_by_date(dataframe,date_x)
    weekday_str = f'{date_y}和{date_x}相比，前者是{weekday_y}而后者为{weekday_x}。从现有数据来看，星期三和星期五会销量更高，而周末会销量较低。'
    print()
    print(weekday_str)
   
    amount_y = get_average_amount_by_weekday(dataframe, weekday_y)
    amount_x = get_average_amount_by_weekday(dataframe, weekday_x)
    weekday_amount_resi = amount_y-amount_x
    print('星期因素差值amount_resi :'+ str(weekday_amount_resi))

    # 节假日归因
    holidays_y = get_holidays_by_date(dataframe,date_y)
    holidays_x = get_holidays_by_date(dataframe,date_x)
    holiday_str = f'{date_y}和{date_x}相比，前者是{holidays_y}而后者为{holidays_x}。从现有数据的规律可以得出，五一和国庆节销量明显高于平时，而元旦和春节销量较低。'
    print()
    print(holiday_str)
    amount_y = get_average_amount_by_holiday(dataframe, holidays_y)
    amount_x = get_average_amount_by_holiday(dataframe, holidays_x)
    print(date_y+' holiday_amount_y:' +str(amount_y))
    print(date_x+' holiday_amount_x:' +str(amount_x))
    holiday_amount_resi = amount_y-amount_x
    print('节假日因素差值amount_resi :'+ str(holiday_amount_resi))

    # wc_night风力归因
    wc_night_y = get_wc_night_by_date(dataframe,date_y)
    wc_night_x = get_wc_night_by_date(dataframe,date_x)
    wc_night_str=f'{date_y}和{date_x}相比，前者风力是{wc_night_y}而后者为{wc_night_x}。从风力归因中可以发现，在大风天气下销量会下滑，而其它不同天气因素销量也会受到影响。'
    print()
    print(wc_night_str)

    amount_y = get_average_amount_by_wc_night(dataframe, wc_night_y)
    amount_x = get_average_amount_by_wc_night(dataframe, wc_night_x)
    print(date_y+' wc_night_y:' +str(amount_y))
    print(date_x+' wc_night_x:' +str(amount_x))
    wc_night_amount_resi = amount_y-amount_x
    print('风力因素差值amount_resi :'+ str(wc_night_amount_resi))

    # 调价归因
    encode_weight_305price_y = get_weight_305pricee_by_date(dataframe,date_y)
    encode_weight_305price_x = get_weight_305pricee_by_date(dataframe,date_x)
    label_y = get_label_305pricee_by_date(dataframe,date_y)
    label_x = get_label_305pricee_by_date(dataframe,date_x)
    
    amount_y = get_predict_amount_by_encoded_305price(encode_weight_305price_y)
    amount_x = get_predict_amount_by_encoded_305price(encode_weight_305price_x)
    print()
    print(date_y+label_y+' encode_weight_305price_y:' +str(encode_weight_305price_y)+' amount: '+str(amount_y))
    print(date_x+label_x+' encode_weight_305price_x:' +str(encode_weight_305price_x)+' amount: '+str(amount_x))
    label_305price_str = f'{date_y}和{date_x}相比，前者是{label_y}而后者{label_x}。调价会明显地影响调价日前两日与后三日的销量，具体表现为如果涨价那么前两日销量会增加，如果降价当日销量大概率会增加，并会持续一小段时间。而其影响的大小与涨价与降价的幅度也同样有关。'
    print(label_305price_str)
    encoded_305price_amount_resi = amount_y-amount_x
    print('调价因素差值encoded_305price_amount_resi :'+ str(encoded_305price_amount_resi))

    ## 综合归因
    # 将它们放入一个字典
    array_base = {
        temperature_str: temperature_amount_resi,
        weekday_str: weekday_amount_resi,
        holiday_str: holiday_amount_resi,
        wc_night_str: wc_night_amount_resi,
        label_305price_str: encoded_305price_amount_resi
    }
    # 计算影响因子
    array = calculate_infra(array_base)
    array = analyze_infra(dataframe, date_y, date_x, array)
    return array

## 工具函数（范围对比）
def get_count_by_dateRange(dataframe, group_by_col, date_y_start, date_y_end):
    # 创建一个空的字典来存储温度统计
    key_count = {}

    # 将date列转换为datetime格式
    dataframe['date'] = pd.to_datetime(dataframe['date'])

    # 筛选出指定日期范围内的数据
    mask = (dataframe['date'] >= date_y_start) & (dataframe['date'] <= date_y_end)
    filtered_df = dataframe.loc[mask]

    # 遍历筛选后的 dataframe 中的每一行
    for _, row in filtered_df.iterrows():
        current_key = row[group_by_col]

        # 如果该key值已经在字典中，则计数加一
        if current_key in key_count:
            key_count[current_key] += 1
        else:
            # 如果该key值不在字典中，则添加，并将计数设为一
            key_count[current_key] = 1

    # 返回温度统计字典
    print(json.dumps(key_count, ensure_ascii=False, indent=4))
    return key_count

def calculate_groupby_mean_to_dict(dataframe, cols_groupby, cols_target):
    """
    计算指定列按另一列分组后的平均值，并将结果转换为字典

    参数:
    dataframe: pandas DataFrame
    cols_groupby: 用于分组的列名
    cols_target: 计算平均值的目标列名

    返回:
    处理后的字典，包含分组列的值作为键，目标列的平均值作为值
    """
    # 计算每个分组的目标列的平均值
    groupby_mean = dataframe.groupby(cols_groupby)[cols_target].mean().reset_index()

    # 将 DataFrame 转换为字典，key 是分组列的值，value 是目标列的平均值
    result_dict = groupby_mean.set_index(cols_groupby).to_dict()[cols_target]
    
    return result_dict

def calculate_mean_value(mean_dict, count_dict):
    """
    计算基于count的加权平均值

    参数:
    mean_dict: dict, 各key值在数据集中的平均销量
    count_dict: dict, 各key值的计数

    返回:
    基于计数的加权平均值
    """
    total_sum = 0
    total_count = 0

    for theKey, count in count_dict.items():
        if theKey in mean_dict:
            mean_sales = mean_dict[theKey]
            total_sum += mean_sales * count
            total_count += count

    if total_count == 0:
        return 0  # 避免除以0的情况

    weighted_average = total_sum / total_count
    return weighted_average

def get_mean_amount_by_date_range(dataframe, start_date, end_date):
    """
    根据日期范围获取总销量数据。

    参数:
    dataframe (pd.DataFrame): 包含销量数据的数据框。
    start_date (str): 起始日期，格式应为 "YYYY-MM-DD"。
    end_date (str): 结束日期，格式应为 "YYYY-MM-DD"。

    返回:
    float: 指定日期范围内的日均销量。
    """
    mask = (dataframe['date'] >= start_date) & (dataframe['date'] <= end_date)
    mean_amount = dataframe.loc[mask, 'amount'].mean()
    return mean_amount

def analyze_range_infra(dataframe, date_y_start, date_y_end, date_x_start, date_x_end, array):
    """
    分析两个时间段内销量变化的归因因素，并返回更新后的影响权重字典。

    参数:
    dataframe (pd.DataFrame): 包含销量数据的数据框。
    date_y_start (str): 第一个时间段的起始日期，格式应为 "YYYY-MM-DD"。
    date_y_end (str): 第一个时间段的结束日期，格式应为 "YYYY-MM-DD"。
    date_x_start (str): 第二个时间段的起始日期，格式应为 "YYYY-MM-DD"。
    date_x_end (str): 第二个时间段的结束日期，格式应为 "YYYY-MM-DD"。
    array (dict): 包含影响因素及其权重的字典，其中键是影响因素名称，值是其对应的权重。

    返回:
    dict: 更新后的影响权重字典，其中包含销量变化的描述和归因分析结果。字典的键是影响因素名称，值是描述影响权重的字符串。
    """
    keys_to_delete = []

    # 获取两个时间段的总销量数据，并计算变化量
    amount_y = get_mean_amount_by_date_range(dataframe, date_y_start, date_y_end) / 10000
    amount_x = get_mean_amount_by_date_range(dataframe, date_x_start, date_x_end) / 10000
    amount_resi = amount_y - amount_x

    # 根据销量变化量进行归因分析
    if amount_resi > 0:  # 销量增长归因
        amount_str = f'{date_y_start}到{date_y_end}和{date_x_start}到{date_x_end}相比，前者日均销量{amount_y:.2f}万，后者日均销量{amount_x:.2f}万。日均销量多了{amount_resi:.2f}万。'
        array = dict(sorted(array.items(), key=lambda item: item[1], reverse=True))  # 倒序重排
        for key in array:
            if array[key] < 0.001:  # 忽略过小的因素
                keys_to_delete.append(key)
    elif amount_resi < 0:  # 销量减少归因
        amount_str = f'{date_y_start}到{date_y_end}和{date_x_start}到{date_x_end}相比，前者日均销量{amount_y:.2f}万，后者日均销量{amount_x:.2f}万。日均销量少了{-amount_resi:.2f}万。'
        for key in array:
            if array[key] > -0.001:
                keys_to_delete.append(key)
    else:  # 销量无变化
        amount_str = f'{date_y_start}到{date_y_end}和{date_x_start}到{date_x_end}相比，前者日均销量{amount_y:.2f}万，后者日均销量{amount_x:.2f}万。日均销量无明显变化。'
        for key in array:
            keys_to_delete.append(key)

    # 删掉反方向的原因
    for key in keys_to_delete:
        del array[key]

    # 更新影响权重字典
    for key in array:
        if array[key] < 0:
            array[key] = -array[key]
        array[key] = f"影响权重{(array[key] * 100):.2f}%"

    # 打印归因分析结果
    # print()
    # print(amount_str)
    array[amount_str] = '归因成功'
    print("归因分析:", json.dumps(array, indent=4, ensure_ascii=False))

    return array

def generate_holiday_count_str(holidays_count_dict):
    """
    根据节假日计数字典生成描述字符串。

    参数:
    holidays_count_dict (dict): 包含节假日计数的字典。

    返回:
    str: 描述节假日计数的字符串。如果字典中只有一个键且为'平时'，则返回'无节假日'。
    """
    if len(holidays_count_dict) == 1 and '平时' in holidays_count_dict:
        return '无任何节假日'
    else:
        holiday_str = "，".join([f"{key}{holidays_count_dict[key]}天" for key in holidays_count_dict.keys()])
        holiday_str = '共有'+holiday_str
        return holiday_str

def generate_week_count_str(week_count_dict):
    """
    根据星期一、星期二至星期天的计数字典生成描述字符串。

    参数:
    week_count_dict (dict): 包含星期一、星期二至星期天的计数字典。

    返回:
    str: 描述星期计数的字符串。会把星期三和星期五分开计数，把星期六和星期天合并计数为周末，把剩下的合并计数为平时。
    """
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"]
    
    # 初始化计数
    weekday_count = 0
    weekend_count = 0
    wednesday_count = 0
    friday_count = 0
    
    # 累加计数
    for day, count in week_count_dict.items():
        if day == "星期三":
            wednesday_count = count
        elif day == "星期五":
            friday_count = count
        elif day in ["星期六", "星期天"]:
            weekend_count += count
        elif day in ["星期一", "星期二", "星期四"]:
            weekday_count += count
    
    # 构建描述字符串
    result_parts = []
    if wednesday_count > 0:
        result_parts.append(f"星期三{wednesday_count}天")
    if friday_count > 0:
        result_parts.append(f"星期五{friday_count}天")
    if weekday_count > 0:
        result_parts.append(f"平时{weekday_count}天")
    if weekend_count > 0:
        result_parts.append(f"周末{weekend_count}天")
    
    return "，".join(result_parts)

def generate_wc_night_count_str(wc_night_count_dict):
    """
    根据夜间风力级数的计数字典生成风力归因描述字符串。

    参数:
    wc_night_count_dict (dict): 包含夜间风力级数的计数字典。

    返回:
    str: 描述夜间风力级数的字符串。把'<3级'和'3~4级'合并计数为低风力情况，而把其它key分开计数。
    """
    # 初始化低风力情况计数
    low_wind_count = 0
    
    # 其他风力级数的计数
    other_wind_counts = {}
    
    # 累加计数
    for level, count in wc_night_count_dict.items():
        if level in ['<3级', '3~4级']:
            low_wind_count += count
        else:
            other_wind_counts[level] = count
    
    # 构建描述字符串
    result_parts = []
    if low_wind_count > 0:
        result_parts.append(f"低风力:{low_wind_count}天")
    for level, count in other_wind_counts.items():
        result_parts.append(f"{level}:{count}天")
    
    return "，".join(result_parts)

def generate_temperature_count_str(temperature_count_dict):
    """
    根据温度的计数字典生成温度描述字符串。

    参数:
    temperature_count_dict (dict): 包含温度的计数字典。

    返回:
    str: 描述温度情况的字符串。会返回最高温度，最低温度，和加权平均温度。
    """
    temperatures = []
    total_count = 0
    weighted_sum = 0
    
    for temp_str, count in temperature_count_dict.items():
        temp = int(temp_str)
        temperatures.append(temp)
        total_count += count
        weighted_sum += temp * count
    
    if total_count == 0:
        return "无温度数据"
    
    max_temp = max(temperatures)
    min_temp = min(temperatures)
    weighted_avg_temp = weighted_sum / total_count
    
    return f"最高温度{max_temp}度，最低温度{min_temp}度，平均约为{weighted_avg_temp:.2f}度"

def generate_label_count_str(label_count_dict):
    """
    根据调价label计数字典生成描述字符串。会把标签分为四大类，涨价利好，涨价利空，降价利好，降价利空。
    如果四个因素的天数都为0，则输出“无日期受调价影响”。

    参数:
    label_count_dict (dict): 包含调价label计数的字典。

    返回:
    str: 描述调价label计数的字符串。
    """
    # 定义涨价和降价相关的标签
    increase_labels_add = ["涨价前两天", "涨价前一天"]  # 涨价导致销量向上波动的情况
    increase_labels_minus = ["涨价当天", "涨价第二天", "涨价第三天", "涨价第四天"]  # 涨价导致销量向下波动的情况
    decrease_labels_add = ["降价当天", "降价第一天", "降价第二天", "降价第三天"]  # 降价导致销量向上波动的情况
    decrease_labels_minus = ["降价前两天", "降价前一天"]  # 降价导致销量向下波动的情况

    # 计算涨价和降价相关标签的总天数
    increase_count_add = sum(label_count_dict.get(label, 0) for label in increase_labels_add)
    increase_count_minus = sum(label_count_dict.get(label, 0) for label in increase_labels_minus)
    decrease_count_add = sum(label_count_dict.get(label, 0) for label in decrease_labels_add)
    decrease_count_minus = sum(label_count_dict.get(label, 0) for label in decrease_labels_minus)

    # 生成描述字符串
    result_str = ""

    if increase_count_add > 0:
        result_str += f"有{increase_count_add}天受涨价前抢购因素影响，"
    if increase_count_minus > 0:
        result_str += f"有{increase_count_minus}天受涨价后的价格因素影响，"
    if decrease_count_add > 0:
        result_str += f"有{decrease_count_add}天受降价利好销量的提振影响，"
    if decrease_count_minus > 0:
        result_str += f"有{decrease_count_minus}天受降价前持币待购的因素影响，"

    # 如果所有因素的天数都为0，输出“无日期受调价影响”
    if not result_str:
        result_str = "无日期受调价影响"
    else:
        # 去掉最后一个逗号
        if result_str.endswith("，"):
            result_str = result_str[:-1]

    return result_str
    

def get_predict_mean_amount_by_encoded_305price(dataframe, date_start, date_end):
    """
    获取dataframe中指定日期区间的encode_weight_305price列的数值之和

    参数:
    date_start (str): 起始日期
    date_end (str): 结束日期

    返回:
    指定日期区间的encode_weight_305price列的数值之和
    """
    # 将日期列转换为datetime类型
    dataframe['date'] = pd.to_datetime(dataframe['date'], format='%Y-%m-%d')
    
    # 将起始日期和结束日期转换为datetime类型
    date_start = pd.to_datetime(date_start, format='%Y-%m-%d')
    date_end = pd.to_datetime(date_end, format='%Y-%m-%d')
    
    # 筛选出指定日期区间的数据
    mask = (dataframe['date'] >= date_start) & (dataframe['date'] <= date_end)
    filtered_df = dataframe.loc[mask].copy()
    
    # 以encode_weight_305price列的数值来预估销量
    filtered_df['encode_weight_305price'] = get_predict_amount_by_encoded_305price(filtered_df['encode_weight_305price'])

    # 计算销量均值
    average_value = filtered_df['encode_weight_305price'].mean()
    
    return average_value
    
## 日期范围对比归因
def compare_by_dateRange(dataframe, date_y_start, date_y_end, date_x_start, date_x_end):
    # 温度归因
    temperature_y_count_dict = get_count_by_dateRange(dataframe,'high', date_y_start, date_y_end)
    temperature_x_count_dict = get_count_by_dateRange(dataframe,'high', date_x_start, date_x_end)

    temperature_y_count_str = generate_temperature_count_str(temperature_y_count_dict)
    temperature_x_count_str = generate_temperature_count_str(temperature_x_count_dict)
    print()
    temperature_str = f'{date_y_start}至{date_y_end},{temperature_y_count_str}。而{date_x_start}至{date_x_end}，{temperature_x_count_str}。根据现有数据回归的情况，温度过高和过低都会带来销量增长，而适宜温度可能会导致销量降低。'
    print(temperature_str)
    
    temperature_mean_dict = calculate_groupby_mean_to_dict(df, 'high', 'amount')
    amount_y = calculate_mean_value(temperature_mean_dict, temperature_y_count_dict)
    amount_x = calculate_mean_value(temperature_mean_dict, temperature_x_count_dict)
    temperature_amount_resi = amount_y-amount_x
    print('温度因素差值amount_resi :'+ str(temperature_amount_resi))

    # weekday星期几归因
    weekday_y_count_dict = get_count_by_dateRange(dataframe,'week', date_y_start, date_y_end)
    weekday_x_count_dict = get_count_by_dateRange(dataframe,'week', date_x_start, date_x_end)

    weekday_y_count_str = generate_week_count_str(weekday_y_count_dict)
    weekday_x_count_str = generate_week_count_str(weekday_x_count_dict)
    print()
    weekday_str = f'{date_y_start}至{date_y_end},共有{weekday_y_count_str}。而{date_x_start}至{date_x_end}，则有{weekday_x_count_str}。基于过往数据经验，星期三和星期五会带来较高销量，而周末的销量略微减少。'
    print(weekday_str)

    week_mean_dict = calculate_groupby_mean_to_dict(df, 'week', 'amount')
    amount_y = calculate_mean_value(week_mean_dict, weekday_y_count_dict)
    amount_x = calculate_mean_value(week_mean_dict, weekday_x_count_dict)
    weekday_amount_resi = amount_y-amount_x
    print('星期因素差值amount_resi :'+ str(weekday_amount_resi))

    # 节假日归因
    holidays_y_count_dict = get_count_by_dateRange(dataframe,'holidays', date_y_start, date_y_end)
    holidays_x_count_dict = get_count_by_dateRange(dataframe,'holidays', date_x_start, date_x_end)

    holiday_y_count_str = generate_holiday_count_str(holidays_y_count_dict)
    holiday_x_count_str = generate_holiday_count_str(holidays_x_count_dict)
    print()
    holiday_str = f'{date_y_start}至{date_y_end},{holiday_y_count_str}。而{date_x_start}至{date_x_end}，{holiday_x_count_str}。从现有数据的规律可以得出，五一和国庆节销量明显高于平时，而元旦和春节销量较低。'
    print(holiday_str)

    holidays_mean_dict = calculate_groupby_mean_to_dict(df, 'holidays', 'amount')
    amount_y = calculate_mean_value(holidays_mean_dict, holidays_y_count_dict)
    amount_x = calculate_mean_value(holidays_mean_dict, holidays_x_count_dict)
    holiday_amount_resi = amount_y-amount_x
    print('节假日因素差值amount_resi :'+ str(holiday_amount_resi))

    # wc_night风力归因
    wc_night_y_count_dict = get_count_by_dateRange(dataframe,'wc_night', date_y_start, date_y_end)
    wc_night_x_count_dict = get_count_by_dateRange(dataframe,'wc_night', date_x_start, date_x_end)

    wc_night_y_count_str = generate_wc_night_count_str(wc_night_y_count_dict)
    wc_night_x_count_str = generate_wc_night_count_str(wc_night_x_count_dict)
    print()
    wc_night_str = f'{date_y_start}至{date_y_end},共有{wc_night_y_count_str}。而{date_x_start}至{date_x_end}，则有{wc_night_x_count_str}。从过往规律来看，大风天气会影响销量。'
    print(wc_night_str)

    wc_night_mean_dict = calculate_groupby_mean_to_dict(df, 'wc_night', 'amount')
    amount_y = calculate_mean_value(wc_night_mean_dict, wc_night_y_count_dict)
    amount_x = calculate_mean_value(wc_night_mean_dict, wc_night_x_count_dict)
    wc_night_amount_resi = amount_y-amount_x
    print('风力因素差值amount_resi :'+ str(wc_night_amount_resi))

    # 调价归因
    label_y = get_count_by_dateRange(dataframe,'encode_label_305price', date_y_start, date_y_end)
    label_x = get_count_by_dateRange(dataframe,'encode_label_305price', date_x_start, date_x_end)
    label_y_str = generate_label_count_str(label_y)
    label_x_str = generate_label_count_str(label_x)
    print()
    label_305price_str = f'{date_y_start}至{date_y_end},共{label_y_str}。而{date_x_start}至{date_x_end}，则{label_x_str}。涨价和降价均会波及前后日期的销量，且都会有正负双向影响，例如涨价前会导致抢购，降价前会导致持币待购，其影响的大小与价格调整的幅度相关。'
    # label_305price_str = f'{date_y}和{date_x}相比，前者是{label_y}而后者{label_x}。调价会明显地影响调价日前两日与后三日的销量，具体表现为如果涨价那么前两日销量会增加，如果降价当日销量大概率会增加，并会持续一小段时间。而其影响的大小与涨价与降价的幅度也同样有关。'
    print(label_305price_str)

    # 基于encoded_305price来预测销量均值
    amount_y = get_predict_mean_amount_by_encoded_305price(df, date_y_start, date_y_end)
    amount_x = get_predict_mean_amount_by_encoded_305price(df, date_x_start, date_x_end)
    encoded_305price_amount_resi = amount_y-amount_x
    print('调价因素差值encoded_305price_amount_resi :'+ str(encoded_305price_amount_resi))

    ## 综合归因
    # 将它们放入一个字典
    array_range = {
        temperature_str: temperature_amount_resi,
        weekday_str: weekday_amount_resi,
        holiday_str: holiday_amount_resi,
        wc_night_str: wc_night_amount_resi,
        label_305price_str: encoded_305price_amount_resi
    }
    # 计算影响因子
    array = calculate_infra(array_range)
    array = analyze_range_infra(dataframe, date_y_start, date_y_end, date_x_start, date_x_end, array)
    return array


# 验证日期格式
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# 获取单日对比
from datetime import datetime
@app.route('/getCause', methods=['GET'])
def get_cause():
    dateY = request.args.get('DateY')
    dateX = request.args.get('DateX')
    
    if not dateY or not dateX:
        return jsonify({'error': 'Please provide two date to compare'}), 400

    if not is_valid_date(dateY) or not is_valid_date(dateX):
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD format.'}), 400

    try:
        result = compare_by_date(df,dateY,dateX)
        # 将结果转换为JSON字符串并解码为中文
        json_result = json.dumps(result, ensure_ascii=False)
        return jsonify(json.loads(json_result))
        #return jsonify(result)
    except FileNotFoundError as fnf_error:
        return jsonify({'error': str(fnf_error)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/getRangeCause', methods=['GET'])
def get_range_cause():
    dateYstart = request.args.get('dateYstart')
    dateYend = request.args.get('dateYend')
    dateXstart = request.args.get('dateXstart')
    dateXend = request.args.get('dateXend')
    
    if not dateYstart or not dateYend or not dateXstart or not dateXend:
        return jsonify({'error': 'Please provide 2 date range to compare'}), 400

    if not is_valid_date(dateYstart) or not is_valid_date(dateYend) or not is_valid_date(dateXstart) or not is_valid_date(dateXend):
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD format.'}), 400

    try:
        result = compare_by_dateRange(df,dateYstart, dateYend, dateXstart, dateXend)
        # 将结果转换为JSON字符串并解码为中文
        json_result = json.dumps(result, ensure_ascii=False)
        return jsonify(json.loads(json_result))
        #return jsonify(result)
    except FileNotFoundError as fnf_error:
        return jsonify({'error': str(fnf_error)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)