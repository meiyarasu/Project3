import pandas as pd
import numpy as np
from pmdarima.arima import ADFTest
from pmdarima import auto_arima
import boto3, io
from get_drug_details import get_selected_drug_data_prediction




def get_predicted_data(drug_code,available_stock):

    drug_data = get_selected_drug_data_prediction(drug_code)
    
    # s3_bucket = 'markk-sagemaker-s3-dev'
    # key2 = 'data/Drug_Event_Profile_Data_25-05-2022.csv'
    # s3 = boto3.client('s3')
    # all_data = s3.get_object(Bucket=s3_bucket, Key=key2)
    # data = pd.read_csv(io.BytesIO(all_data['Body'].read()), low_memory=False)

    data = pd.read_csv('Drug_Event_Profile_Data_25-05-2022.csv')

    
    df1=data[['Week_No','PDE_DRUG_TYPE_CD','PDE_DRUG_CD','PDE_DRUG_CLASS_CD','PDE_DRUG_QTY_DIS']]
    df1 = df1[df1['PDE_DRUG_CD']==drug_code]
    df1['total_qty'] = df1.groupby(['Week_No', 'PDE_DRUG_CD', 'PDE_DRUG_TYPE_CD','PDE_DRUG_CLASS_CD'])['PDE_DRUG_QTY_DIS'].transform(lambda x: x.sum())
    df1 = df1.drop_duplicates(subset=['Week_No', 'PDE_DRUG_CD', 'PDE_DRUG_TYPE_CD','PDE_DRUG_CLASS_CD'])
    df1.sort_values(by=['Week_No'], inplace=True, ascending=True)
    df2=df1[['Week_No','total_qty']]
    df3 = df2[['Week_No', 'total_qty']].set_index('Week_No')
    train = df3[:50]
    test = df3[-2:]
    arima_model = auto_arima(train , start_p=0 , d= 1 , start_q=0,
                                            max_p=5 , max_d=5 , max_q=5,
                                            start_P=0 ,D=1, start_Q=0 ,
                                            max_P=5 ,max_D=5 , max_Q=5 ,
                                            m=13 , seasonal=False,
                                            trace=True, suppress_warnings=True,
                                            stepwise=True, random_state=20, n_fits=50)
    prediction = pd.DataFrame(arima_model.predict(n_periods = 2),index = test.index)
    prediction.columns = ['Qty']
    prediction_compare = pd.concat([prediction, test] , axis= 1 , join = 'inner')
    prediction_compare = prediction_compare.fillna(0)
    prediction_compare = prediction_compare.replace(np.nan, 0)
    
    reorder_point = drug_data['REORDER_POINT']
    reorder_qty = drug_data['ORDER_QTY_EOQ']
    safety_stock = drug_data['SAFETY_STOCK']
    if available_stock < reorder_point:
        predicted_reorder = "Yes"
        # print("Predicted Reorder: ", predicted_reorder)
    else:
        predicted_reorder = "No"
    #     print("Predicted Reorder: ", predicted_reorder)
    
    # print("Predicted demand for next two weeks: ", [round(prediction_compare['Qty'].values[0],0), round(prediction_compare['Qty'].values[1],0)])
    # print("Re-Order Point: ", reorder_point)

    # print("Re-order quantity: ", reorder_qty)
    # print("Safety Stock: ", safety_stock)

    return {'predicted_reorder':predicted_reorder,'prediction_next_two_weeks': str(round(prediction_compare['Qty'].values[0],0)) +', ' + str(round(prediction_compare['Qty'].values[1],0)),\
         'reorder_point':reorder_point,'reorder_qty':reorder_qty,'safety_stock': safety_stock }