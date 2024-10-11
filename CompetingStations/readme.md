# 竞争站点价格分析
CompetingStationPrice_Utils.py            # 竞争站点的价格工具，从竞争站点数组中获得价格
CompetingStationsPrice_XGBoost            # 两阶段预测销量（先用prophet捕捉节日特征，再用XGBoost预测，最后用SHAP解释）
CompetingStationsPrice_AnalyzeFactors     # 看看高德数据里的车流量和进站率，会不会受竞争站点价格影响（不会）
CompetingStationsPrice_ChangePrice        # 量化竞争站点变化价格对我方销量的影响
CompetingStationsPrice_Dowhy              # 因果推断，竞争站点价差、或价格，或价格变化是否对我方整体销量/石油/柴油构成影响
CompetingStationsPrice_AvgVolumeFactor    # 单均柴油加油量影响因子分析
CompetingStationsPrice_ForecastOrderCount  # 通过车流量能否准确预测订单数

# 回归模型
Reg_CarFlow                                      # 使用车流量回归销量，得到残差网络。找出与车流量无关的要素，是否可以解释残差值。
XGB_forecast_Liters                               # 使用XGB通过竞争站价格、本站价格、价差、站外车流量来预测加油总升数