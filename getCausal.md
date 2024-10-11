# getCausal归因分析

## 注意事项
    目前从Data/.csv里读数据，但稍稍修改代码把数据导入pandas的df也没问题。
    目前仅支持.csv中包括的时间段内的数据查询。目前只有20230101至20231230的数据。

## 依赖文件
归因只用到了以下两个文件    
    1. getCausal.py  #核心归因代码  
    2. Data/结果1_全站按日期分组_2023全年.csv  #数据来源    


## 如何部署
    1.登陆服务器    
    2.conda activate pyCausal       #pyCausal是我取的环境名，目前在服务器端已经用conda建好了环境，也安装了所依赖的flask库   
    3.nohup python getCausal.py > log.log 2>&1 &        #跑起来getCausal服务，默认部署在端口5000上  


## 接口
仅示例，注意更改IP地址。

### 单日归因
    http://192.168.20.45:5000/getCause?DateY=2023-05-01&DateX=2023-5-5
      DateY(str)：YYYY-MM-DD格式，待分析日
      DateX(str)：YYYY-MM-DD格式，对比日

### 时间段归因
    http://192.168.20.45:5000/getRangeCause?dateYstart=2023-05-01&dateYend=2023-5-5&dateXstart=2023-03-02&dateXend=2023-03-09
      dateYstart(str)：YYYY-MM-DD格式，待分析时间段开始日期
      dateYend(str)：YYYY-MM-DD格式，待分析时间段结束日期
      dateXstart(str)：YYYY-MM-DD格式，对比时间段开始日期
      dateXend(str)：YYYY-MM-DD格式，对比时间段结束日期

### 输出格式
    会输出性质判断（如销量增长），同时会判断两天之间日均销量是由哪个因素造成的，各因素影响的权重分别是多少。
    {   
        'causal_type': '销量增长',
        'success': True,
        'conclusion': '2023-1-3到2023-1-4和2023-2-4到2023-2-5相比，前者日均销量32911.16万，后者日均销量27906.63万。日均销量多了5004.53万。',
        'reseons': 
            {
                '调价': {
                    'subject': '调价',            
                    'analysis': '2023-1-3至2023-1-4,共有1天受涨价前抢购因素影响，有1天受涨价后的价格因素影响。而2023-2-4至2023-2-5，则有2天受涨价后的价格因素影响。涨价和降价均会波及前后日期的销量，且都会有正负双向影响，例如涨价前会导致抢购，降价前会导致持币待购，其影响的大小与价格调整的幅度相关。',
                    'resi': 39728353.9693926,
                     'weight': 0.6575784952154211},
                '星期几': {
                    'subject': '星期几',
                    'analysis': '2023-1-3至2023-1-4,共有星期三1天，平时1天。而2023-2-4至2023-2-5，则有周末1天。基于过往数据经验，星期三和星期五会带来较高销量，而周末的销量略微减少。',
                    'resi': 16245871.710576952,
                    'weight': 0.268899534099356},
                '温度': {
                    'subject': '温度',
                    'analysis': '2023-1-3至2023-1-4,最高温度12度，最低温度9度，平均约为10.50度。而2023-2-4至2023-2-5，最高温度12度，最低温度11度，平均约为11.50度。根据现有数据回归的情况，温度过高和过低都会带来销量增长，而适宜温度可能会导致销量降低。',
                    'resi': 4441913.622727215,
                    'weight': 0.07352197068522291
                    }
            }
   }

## 特征构建
    code_holidays       # 没用
    encoded_holidays    # encoded_holidays是对holidays列的特征构建，载入全部数据后，以['holidays']列为分组，取组内销量平均值，从低到高排序值。
    encoded_305_price        # 调价日的调价幅度特征 305_price 的价格变动的那天，对前一天求差值再放大10倍。例如：7.54 涨到7.74，那么那一天的的值为(7.74-7.54)*10=2。如果是降价则为负数。
    encode_label_305price       # 调价日向前两天和后两天的扩散特征， 会把其前两天和后三天标识上。方便计算encode_weight_305price
    encode_weight_305price      # 基于扩散加权的调价特征，对 encoded_305_price进一步做特征构建。将 encoded_305_price值向前两天做扩散。往前第一天会对encoded_305_price取负号，往前第二天会对encoded_305_price取负号再乘50%。将 encoded_305_price向后三天做扩散，其第一天是 encoded_305_price*0.75. 第二天是第一天的0.75，第三天是第二天的0.75如此来构建特征。
    305_order_cnt        # 305号油的订单量
    305_amount        # 305号油的amount总销量额
    305_discountAmount        # 没用
    305_refuelLiters        # 没用
    313_price       # 313号油的价格       
    encoded_313_price       # 没用
    313_order_cnt       # 313号油的订单量        
    313_amount      # 313号油的amount总销量额        
    313_discountAmount      # 没用        
    313_refuelLiters        # 没用