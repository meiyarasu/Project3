import pandas as pd
import boto3, io, os

s3_bucket = 'markk-sagemaker-s3-dev'
key2 = 'data/Drug_Level_data.csv'
s3 = boto3.client('s3', aws_access_key_id = os.environ['aws_key'],
    aws_secret_access_key = os.environ['aws_sec'],
    region_name = 'ap-south-1')
all_data = s3.get_object(Bucket=s3_bucket, Key=key2)
df_drug_data = pd.read_csv(io.BytesIO(all_data['Body'].read()), low_memory=False)

df_drug_data = pd.read_csv('Drug_Level_data.csv')

def get_all_drugs():
    return df_drug_data['PDE_DRUG_CD'].tolist()

def get_selected_drug_data(drug_code):
    drug_data = df_drug_data[df_drug_data['PDE_DRUG_CD']==drug_code]
    if not drug_data.empty:
        drug_data = drug_data.iloc[0]
        pde_drug_cd = drug_data['PDE_DRUG_CD']
        total_52week_demand = drug_data['TOTAL_52WEEK_DEMAND']
        total_cost = drug_data['TOTAL_COST']
        avg_weekly_demand = drug_data[ 'AVG_WEEKLY_DEMAND']
        stddevdemand = drug_data[ 'STDDEVDEMAND']
        average_lead_time = drug_data['AVERAGE_LEAD_TIME']
        order_frequency = drug_data['Order_Frequency']
        max_weekly_demand = drug_data['Max_Weekly_Demand']
        demand_category = drug_data['Demand_Category']
        cost_per_unit = drug_data['COST_PER_UNIT']
        fixed_ordering = drug_data['Fixed/Ordering Cost (10% of Total)']
        holding_cost = drug_data['Holding Cost (25% of total)']
        order_qty_eoq = drug_data['ORDER_QTY_EOQ']
        safety_stock = drug_data['SAFETY_STOCK']
        volatility_ratio = drug_data['VOLATILITY_RATIO']
        norm_volatility_ratio = drug_data['NORM_VOLATILITY_RATIO']
        norm_cost_per_unit = drug_data['NORM_COST_PER_UNIT']
        reorder_point = drug_data['REORDER_POINT']
        demand_volatility = drug_data['DEMAND_VOLATILITY']
        cost_cat_tag = drug_data['COST_CAT_TAG']
        return drug_data[['Demand_Category','COST_CAT_TAG','DEMAND_VOLATILITY','COST_PER_UNIT','AVG_WEEKLY_DEMAND','Max_Weekly_Demand']].to_dict()
    else:
        return {"output":None}

def get_selected_drug_data_prediction(drug_code):
    drug_data = df_drug_data[df_drug_data['PDE_DRUG_CD']==drug_code]
    if not drug_data.empty:
        drug_data = drug_data.iloc[0]
        return drug_data.to_dict()
    else:
        return {"output":None}