"""AR(2)、Yule–Walker、ARMA 选择与留出样本预测。"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima_process import arma_generate_sample
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from common import table, figure, plt

def run(out,data_file=None):
    rng=np.random.default_rng(123456)
    x=arma_generate_sample([1,-.6,.4],[1],1200,burnin=300,distrvs=rng.standard_normal)
    train,test=x[:1000],x[1000:]
    rho,_=sm.regression.yule_walker(train,order=2,method="mle")
    table(out,"SIMULATED_AR2",{"t":np.arange(len(x)),"value":x,"split":["train"]*1000+["test"]*200})
    table(out,"YW_coefficients",{"lag":[1,2],"truth":[.6,-.4],"estimate":rho})
    candidates=[];models={}
    for p,q in [(1,0),(2,0),(1,1),(2,1)]:
        fit=ARIMA(train,order=(p,0,q),trend="c").fit()
        converged=bool(fit.mle_retvals.get("converged",False))
        candidates.append({"p":p,"q":q,"AIC":fit.aic,"BIC":fit.bic,"converged":converged})
        if converged: models[(p,q)]=fit
    if not models: raise RuntimeError("候选模型均未收敛")
    best=min(models,key=lambda k:models[k].bic);fit=models[best]
    # 固定训练窗，不把测试观测带回模型；这是 1–200 步固定起点预测。
    pred=fit.get_forecast(len(test));interval=np.asarray(pred.conf_int())
    table(out,"holdout_forecast",{"horizon":np.arange(1,len(test)+1),"actual":test,
          "forecast":pred.predicted_mean,"lower95":interval[:,0],"upper95":interval[:,1]})
    table(out,"model_selection",candidates)
    fig,ax=plt.subplots(1,2,figsize=(9,3.6));plot_acf(train,lags=20,ax=ax[0]);plot_pacf(train,lags=20,method="ywm",ax=ax[1]);figure(out,"ACF_PACF")
    return {"data":"SIMULATED AR(2)","selected_order":[best[0],0,best[1]],
            "forecast_MSE":float(np.mean((test-pred.predicted_mean)**2)),"seed":123456}
