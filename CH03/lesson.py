"""公制回归与出版社匿名 A 公司 CAPM。"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from common import ROOT, table, figure, plt

def capm_data(path):
    d = pd.read_csv(path)
    cols = ["stock_price", "market_index", "risk_free_rate"]
    if not {"Date",*cols}.issubset(d): raise ValueError("缺少 Date 或价格、利率字段")
    d["Date"] = pd.to_datetime(d.Date, errors="raise")
    if d.Date.isna().any() or d.Date.duplicated().any() or not d.Date.is_monotonic_increasing:
        raise ValueError("日期须非缺失、严格递增且不重复")
    d[cols] = d[cols].apply(pd.to_numeric, errors="raise")
    flags = d[cols].isna().any(axis=1)
    # 仅为复现出版社正文案例，按行插值；不外推端点。
    d[cols] = d[cols].interpolate(method="linear",limit_area="inside")
    if not np.isfinite(d[cols]).all().all() or (d[["stock_price","market_index"]] <= 0).any().any():
        raise ValueError("数据仍有缺失、非有限值或非正价格")
    r = pd.DataFrame({"date":d.Date.iloc[1:].to_numpy(),
         "stock":np.diff(np.log(d.stock_price)),"market":np.diff(np.log(d.market_index)),
         "rf":d.risk_free_rate.iloc[1:].to_numpy()/100/365})
    r["stock_excess"] = r.stock-r.rf; r["market_excess"] = r.market-r.rf
    return r, pd.DataFrame({"date":d.Date,"interpolated":flags})

def run(out, data_file=None):
    cars=pd.read_csv(ROOT/"CH03/data/mtcars.csv")
    x=cars.wt*.45359237; y=cars.mpg*1.609344/3.785411784
    model=sm.OLS(y,sm.add_constant(x)).fit()
    table(out,"mtcars_metric_coefficients",{"term":["intercept","weight_t"],"estimate":model.params})
    r,flags=capm_data(data_file or ROOT/"CH03/data/stock_data.csv")
    fit=sm.OLS(r.stock_excess,sm.add_constant(r.market_excess)).fit()
    robust=fit.get_robustcov_results(cov_type="HAC",maxlags=5)
    table(out,"publisher_CAPM_coefficients",{"term":["alpha","beta"],"estimate":fit.params,
          "OLS_standard_error":fit.bse,"HAC_standard_error":robust.bse})
    table(out,"publisher_CAPM_returns",r);table(out,"interpolation_flags",flags)
    fig,ax=plt.subplots(1,2,figsize=(9,3.6))
    ax[0].scatter(x,y);ax[0].plot(np.sort(x),model.predict(sm.add_constant(np.sort(x))))
    ax[0].set(xlabel="Weight (tonnes)",ylabel="Fuel efficiency (km/l)")
    ax[1].scatter(r.market_excess,r.stock_excess,s=8)
    ax[1].set(xlabel="Market excess log return",ylabel="Company A excess log return")
    figure(out,"regressions")
    return {"data":"mtcars 与出版社匿名 A 公司案例", "interpolated_rows":int(flags.interpolated.sum()),
            "CAPM_alpha":float(fit.params.iloc[0]),"CAPM_beta":float(fit.params.iloc[1]),
            "rf_convention":"正文教学近似：年化百分数 / 100 / 365；从对数收益中扣除"}
