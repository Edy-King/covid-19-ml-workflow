import json, os, time
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    average_precision_score, brier_score_loss, balanced_accuracy_score, confusion_matrix,
    matthews_corrcoef, precision_recall_curve, roc_curve)
from sklearn.calibration import calibration_curve

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'covid_data_2020-2021.csv'
OUT=ROOT/'rigorous_temporal_holdout'; OUT.mkdir(exist_ok=True)
N=5_861_480
FEATURES=['cough','fever','sore_throat','shortness_of_breath','head_ache','symptom_count','has_any_symptom','has_multiple_symptoms','age_60_and_above_yes','gender_female','gender_male','test_indication_abroad','test_indication_contact with confirmed','test_indication_other','test_month','test_dayofweek']
X=np.empty((N,len(FEATURES)),dtype=np.float32); y=np.empty(N,dtype=np.int8); dates=np.empty(N,dtype='datetime64[D]')
offset=0
for ch in pd.read_csv(DATA,chunksize=250000,low_memory=False):
    n=len(ch); s=slice(offset,offset+n)
    symptoms=ch[['cough','fever','sore_throat','shortness_of_breath','head_ache']].to_numpy(dtype=np.float32)
    sc=symptoms.sum(axis=1)
    gender=ch.gender.astype(str).str.lower(); ind=ch.test_indication.astype(str).str.lower(); d=pd.to_datetime(ch.test_date)
    X[s]=np.column_stack([symptoms,sc,sc>0,sc>=2,ch.age_60_and_above.astype(str).str.lower().eq('yes'),gender.eq('female'),gender.eq('male'),ind.eq('abroad'),ind.eq('contact with confirmed'),ind.eq('other'),d.dt.month,d.dt.dayofweek]).astype(np.float32)
    y[s]=ch.corona_result.map({'Negative':0,'Positive':1}).to_numpy(dtype=np.int8); dates[s]=d.to_numpy(dtype='datetime64[D]'); offset+=n
assert offset==N and not np.isnan(X).any()

# Pre-specified whole-date partitions: ~75% development, ~10% validation, ~15% final temporal holdout.
DEV_END=np.datetime64('2021-03-03'); VAL_END=np.datetime64('2021-08-07')
dev=dates<=DEV_END; val=(dates>DEV_END)&(dates<=VAL_END); hold=dates>VAL_END

model=RandomForestClassifier(n_estimators=300,max_depth=18,min_samples_leaf=10,max_features='sqrt',class_weight='balanced_subsample',n_jobs=max((os.cpu_count() or 2)-1,1),random_state=42)
t=time.time(); model.fit(X[dev],y[dev]); fit_seconds=time.time()-t
val_raw=model.predict_proba(X[val])[:,1]

# Calibration and threshold selection use validation data only.
cal=IsotonicRegression(out_of_bounds='clip',y_min=0,y_max=1).fit(val_raw,y[val])
val_prob=cal.predict(val_raw)
candidate=np.unique(np.quantile(val_prob,np.linspace(0,1,1001)))
best_threshold=max(candidate,key=lambda z:f1_score(y[val],val_prob>=z,zero_division=0))
val_pred=val_prob>=best_threshold

# Final holdout opened once after all choices are fixed.
hold_raw=model.predict_proba(X[hold])[:,1]; hold_prob=cal.predict(hold_raw); hold_pred=hold_prob>=best_threshold

def save_predictions(mask, raw_prob, calibrated_prob, pred, filename):
    rows=pd.DataFrame({
        'row_index':np.flatnonzero(mask),
        'test_date':dates[mask].astype(str),
        'y_true':y[mask].astype(np.int8),
        'raw_probability':raw_prob.astype(np.float32),
        'calibrated_probability':calibrated_prob.astype(np.float32),
        'prediction_at_frozen_threshold':pred.astype(np.int8),
    })
    rows.to_csv(OUT/filename,index=False,compression='gzip')

def met(yy,prob,pred):
    tn,fp,fn,tp=confusion_matrix(yy,pred).ravel()
    return {'accuracy':accuracy_score(yy,pred),'precision':precision_score(yy,pred,zero_division=0),'recall':recall_score(yy,pred,zero_division=0),'specificity':tn/(tn+fp),'f1':f1_score(yy,pred,zero_division=0),'balanced_accuracy':balanced_accuracy_score(yy,pred),'roc_auc':roc_auc_score(yy,prob),'average_precision':average_precision_score(yy,prob),'brier_score':brier_score_loss(yy,prob),'mcc':matthews_corrcoef(yy,pred),'tn':int(tn),'fp':int(fp),'fn':int(fn),'tp':int(tp)}
save_predictions(val,val_raw,val_prob,val_pred,'validation_predictions.csv.gz')
save_predictions(hold,hold_raw,hold_prob,hold_pred,'untouched_temporal_holdout_predictions.csv.gz')

result={'design':{'development':'2020-03-20 to 2021-03-03','validation':'2021-03-04 to 2021-08-07','untouched_temporal_holdout':'2021-08-08 to 2021-10-11','development_n':int(dev.sum()),'validation_n':int(val.sum()),'holdout_n':int(hold.sum()),'development_prevalence':float(y[dev].mean()),'validation_prevalence':float(y[val].mean()),'holdout_prevalence':float(y[hold].mean()),'threshold_selection':'maximum validation F1 after validation-only isotonic calibration','selected_threshold':float(best_threshold),'fit_seconds':fit_seconds,'prediction_files':['validation_predictions.csv.gz','untouched_temporal_holdout_predictions.csv.gz']},'validation':met(y[val],val_prob,val_pred),'holdout':met(y[hold],hold_prob,hold_pred)}
(OUT/'rigorous_temporal_results.json').write_text(json.dumps(result,indent=2))
pd.DataFrame([{'partition':'development','start':'2020-03-20','end':'2021-03-03','n':int(dev.sum()),'prevalence':float(y[dev].mean())},{'partition':'validation','start':'2021-03-04','end':'2021-08-07','n':int(val.sum()),'prevalence':float(y[val].mean())},{'partition':'untouched temporal holdout','start':'2021-08-08','end':'2021-10-11','n':int(hold.sum()),'prevalence':float(y[hold].mean())}]).to_csv(OUT/'partition_summary.csv',index=False)

# Holdout plots.
fig,axs=plt.subplots(1,3,figsize=(16,4.6))
fpr,tpr,_=roc_curve(y[hold],hold_prob); axs[0].plot(fpr,tpr,label=f"AUC={result['holdout']['roc_auc']:.3f}"); axs[0].plot([0,1],[0,1],'k--'); axs[0].set(xlabel='False-positive rate',ylabel='True-positive rate',title='Untouched holdout ROC'); axs[0].legend()
p,r,_=precision_recall_curve(y[hold],hold_prob); axs[1].plot(r,p,label=f"AP={result['holdout']['average_precision']:.3f}"); axs[1].axhline(y[hold].mean(),ls='--',color='k',label=f"Prevalence={y[hold].mean():.3f}"); axs[1].set(xlabel='Recall',ylabel='Precision',title='Untouched holdout precision–recall'); axs[1].legend()
pt,pp=calibration_curve(y[hold],hold_prob,n_bins=10,strategy='quantile'); axs[2].plot(pp,pt,'o-'); axs[2].plot([0,1],[0,1],'k--'); axs[2].set(xlabel='Mean calibrated probability',ylabel='Observed proportion',title='Untouched holdout calibration')
fig.tight_layout(); fig.savefig(OUT/'untouched_temporal_holdout.png',dpi=220); plt.close(fig)
print(json.dumps(result,indent=2),flush=True)
