# 竞争站点价格分析
CompetingStationPrice_Utils.py            # 竞争站点的价格工具，从竞争站点数组中获得价格
CompetingStationsPrice_XGBoost            # 两阶段预测销量（先用prophet捕捉节日特征，再用XGBoost预测，最后用SHAP解释）
CompetingStationsPrice_AnalyzeFactors     # 看看高德数据里的车流量和进站率，会不会受竞争站点价格影响（不会）