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