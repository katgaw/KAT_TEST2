import pandas as pd
import numpy as np

def data_transform(df_all,first_day_future):
    df_all['CPI']=df_all['CPI'].astype('float')
    df_all['Employment']=df_all['Employment'].astype('float')

    # Add future row and Shift X columns
    df_future_row=pd.DataFrame({0: df_all.reset_index().columns,1:df_all.reset_index().iloc[-1,:]}).T
    
    df_future_row.columns=df_future_row.iloc[0,:]
    
    df_future_row=df_future_row.drop(0).drop(columns=['index'])
    df_future_row.insert(0,'',pd.to_datetime(first_day_future).strftime("%Y-%m-%d"))
    df_future_row.set_index(df_future_row.iloc[:,0],inplace=True)
    df_future_row=df_future_row.drop(columns='')
    if 'level_0' in df_future_row.columns:
        df_future_row=df_future_row.drop(columns='level_0')
    if 'index' in df_all.columns:
        df_all=df_all.drop(columns='index')

    df_with_future=pd.concat([df_all,df_future_row],axis=0)
    df_with_future.index.names=['date']
    df_with_future.index=pd.to_datetime(df_with_future.index).strftime("%Y-%m-%d")
    df_with_future=df_with_future.shift()
    df_final=df_with_future.interpolate(method='linear',limit_direction='both', 
                                                limit=100).bfill().ffill()
    df_final['name']=np.repeat(df_final['id'].iloc[:,0].dropna()[0:1][0],len(df_final))
    df_final=df_final.drop(columns='id')
    #Data transformation coin_dummy, time_variables, shift X, iso_week
    df_final['name_no']=pd.get_dummies(df_final['name'],dtype='int')
    df_final.index=pd.to_datetime(df_final.index, utc=True)
    df_final['Day']=df_final.index.day
    df_final['Month']=df_final.index.month
    df_final['Year']=df_final.index.year
    seasonal_dummy=pd.get_dummies(df_final.index.day,dtype='int')
    seasonal_dummy.index=df_final.index
    seasonal_dummy.columns=[str('day_'+str(value)) for value in seasonal_dummy.columns]
    reframed=pd.concat([df_final,seasonal_dummy],axis=1).drop(columns='name')
    print(reframed.iloc[-5:,:])
    reframed=reframed.reset_index().drop(columns=['date'])
    reframed_lags=reframed.copy()
    reframed_lags['lag1'] = reframed_lags['prices'].iloc[-1]
    reframed_lags['lag2'] = reframed_lags['prices'].iloc[-2]

    # Use the last observed values for lag features
    for i in range(1, len(reframed_lags)):
        reframed_lags.loc[reframed_lags.index[i], 'lag1'] = reframed_lags.loc[reframed_lags.index[i-1], 'prices'] if 'prices' in reframed_lags.columns else reframed_lags.loc[reframed_lags.index[i-1], 'lag1']
        reframed_lags.loc[reframed_lags.index[i], 'lag2'] = reframed_lags.loc[reframed_lags.index[i-1], 'lag1']
    return reframed_lags, df_final