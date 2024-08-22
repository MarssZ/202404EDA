# 归因模型： 
## 江苏AIGC归因
    getCausal.md                         #江苏AIGC归因readme：只看这个，下面不用看
    ModelAttribution_Linear              #归因模型：线性归因 
    ModelAttribution_Classification      #归因模型：多分类归因

# EDA
    EDA_corr_column                         #上传一个表格，自动找到与目标列最相关的因子

# Tools工具类
    DataInsight_Correlation_Corr.ipynb                     #相关性计算 
    DataInsight_SinglePointInsight_OutstandingNo1.ipynb    #异常值模型：不寻常的最大值

## 第一步：特征构建
    Features_Construction.ipynb 特征构建的测试文件
    GetWeather.ipynb 通过API获取天气数据

## 第二步：特征描述
    Test_Hist.ipynb     #直方图，用来显示单一连续变量自身的分布情况
    Test_OneWayANOVA    #单因素（分类）方差检验ANOVA，用来检验一个分类自变量（如天气情况）和一个连续自变量（如销量）之间是否存在关系。
    Test_TwoWayLinear   #分析两个连续变量是否线性相关
    Test_timeSeries     #分析时间序列
    Test_Spearman.ipynb #分析两个连续变量是否spearman相关

## 第三步：回归预测
    Test_Prophet 使用Prophet来预测未来价格走势，


