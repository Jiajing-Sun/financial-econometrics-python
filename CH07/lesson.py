"""核函数、历史 DAX 密度与非参数条件均值。"""
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
from common import ROOT, table, figure, plt

def local_linear(x,y,grid,bandwidth):
    if bandwidth<=0:raise ValueError("带宽必须为正")
    x=np.asarray(x);y=np.asarray(y);result=[]
    for at in grid:
        dx=x-at;w=np.exp(-.5*(dx/bandwidth)**2)
        X=np.column_stack([np.ones(len(x)),dx])
        beta=np.linalg.lstsq(X*np.sqrt(w[:,None]),y*np.sqrt(w),rcond=None)[0]
        result.append(beta[0])
    return np.asarray(result)

def run(out,data_file=None):
    d=pd.read_csv(ROOT/"CH07/data/EuStockMarkets.csv");r=100*np.diff(d.DAX)/d.DAX.to_numpy()[:-1]
    grid=np.linspace(r.min()-1,r.max()+1,500);kde=gaussian_kde(r,bw_method="scott")
    table(out,"DAX_density",{"return_percent":grid,"density":kde(grid)})
    u=np.linspace(-1.5,1.5,601)
    table(out,"kernels",{"u":u,"uniform":.5*(abs(u)<=1),"Epanechnikov":.75*np.maximum(1-u*u,0),"Gaussian":np.exp(-u*u/2)/np.sqrt(2*np.pi)})
    plt.plot(u,.5*(abs(u)<=1),label="Uniform")
    plt.plot(u,.75*np.maximum(1-u*u,0),label="Epanechnikov")
    plt.plot(u,np.exp(-u*u/2)/np.sqrt(2*np.pi),label="Gaussian")
    plt.xlabel("u");plt.ylabel("Kernel K(u)");plt.legend();figure(out,"kernel_functions")
    # 使用同一历史样本的 FTSE、DAX 收益，展示二维分布与条件均值。
    x=100*np.diff(d.FTSE)/d.FTSE.to_numpy()[:-1];y=r
    gx=np.linspace(np.quantile(x,.02),np.quantile(x,.98),150)
    bw=1.06*np.std(x,ddof=1)*len(x)**(-.2)
    fitted=local_linear(x,y,gx,bw)
    table(out,"DAX_given_FTSE",{"FTSE_return_percent":gx,"DAX_conditional_mean":fitted})
    fig,ax=plt.subplots(1,2,figsize=(9,3.6));ax[0].hist(r,bins=40,density=True,alpha=.4);ax[0].plot(grid,kde(grid));ax[0].set_xlabel("DAX return (%)")
    ax[1].scatter(x,y,s=5,alpha=.2);ax[1].plot(gx,fitted);ax[1].set(xlabel="FTSE return (%)",ylabel="DAX return (%)");figure(out,"nonparametric")
    return {"data":"EuStockMarkets 1991—1998 历史样本；按 observation 索引，无伪造日期", "n":len(r),
            "density_bandwidth":"SciPy Scott；不同于 R density 的默认带宽", "regression_bandwidth":float(bw)}
