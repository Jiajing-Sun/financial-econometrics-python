"""树、随机森林与逻辑回归的滚动样本外比较。"""
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, brier_score_loss
from common import table, figure, plt

def stock_panel(seed=123,N=40,T=42):
    rng=np.random.default_rng(seed);rate=np.zeros(T)
    for t in range(1,T):rate[t]=.8*rate[t-1]+rng.normal(0,.2)
    # 用生成机制的无条件标准差缩放，不用未来样本估计均值或尺度。
    rate=rate/(.2/np.sqrt(1-.8**2))
    d=pd.DataFrame({'month':np.repeat(np.arange(1,T+1),N),'id':np.tile(np.arange(1,N+1),T)})
    d['rate']=rate[d.month.to_numpy()-1];d['pe']=np.maximum(rng.normal(15,5,len(d)),1)
    d['mom']=rng.normal(size=len(d));d['vol']=np.exp(rng.normal(0,.3,len(d)))
    signal=-.02*d.pe-.5*d.rate+.3*d.mom-.1*d.vol+np.where((d.rate<0)&(d.pe>18),-.2,0)
    d['ret_fwd']=.02*signal+rng.normal(0,.05,len(d));d['up']=(d.ret_fwd>0).astype(int)
    return d

def run(out,data_file=None):
    d=stock_panel();features=['rate','pe','mom','vol'];predictions=[];windows=[]
    # 特征在月末 m 已知，ret_fwd 在月末 m+1 揭示。预测时 m-1 标签已经可得。
    for t in range(25,43):
        train=d[d.month.between(t-24,t-1)];test=d[d.month==t]
        models={'tree':DecisionTreeClassifier(min_samples_split=30,min_samples_leaf=10,ccp_alpha=.005,random_state=123),
                'forest':RandomForestClassifier(n_estimators=100,min_samples_leaf=10,max_features='sqrt',random_state=123,n_jobs=1),
                'logistic':make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000))}
        windows.append({'prediction_month':t,'training_feature_first':t-24,'training_feature_last':t-1,'latest_training_label_known_at':t})
        for name,model in models.items():
            model.fit(train[features],train.up);proba=model.predict_proba(test[features])[:,list(model.classes_).index(1)]
            predictions.extend({'model':name,'month':t,'id':int(i),'probability_up':float(p),'actual':int(y)} for i,p,y in zip(test.id,proba,test.up))
    pred=pd.DataFrame(predictions);metrics=[]
    for name,g in pred.groupby('model'):
        metrics.append({'model':name,'Brier':brier_score_loss(g.actual,g.probability_up),
                        'AUC':roc_auc_score(g.actual,g.probability_up),'accuracy':np.mean((g.probability_up>.5)==g.actual)})
    table(out,'SIMULATED_stock_panel',d);table(out,'time_windows',windows)
    table(out,'SIMULATED_out_of_sample',pred);table(out,'model_metrics',metrics)
    pd.DataFrame(metrics).set_index('model').Brier.plot.bar(rot=0,figsize=(7,3.5));plt.ylabel('Out-of-sample Brier score');figure(out,'model_comparison')
    return {'data':'SIMULATED：40 只股票、42 个月','models':3,'training_window_months':24,
            'out_of_sample_rows_per_model':720,'tuning':'预先固定参数，测试窗未用于选择模型或阈值',
            'R_difference':'scikit-learn 与 rpart 的剪枝准则及默认设置不同，不要求树结构逐节点相同'}
