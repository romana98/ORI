import numpy as np
import pandas as pd
from src.get_insights_from_KPIs import get_insights
from sklearn.preprocessing import StandardScaler

# ignore warnings
import warnings
warnings.filterwarnings(action="ignore")


def load():
    print("Started data load and process!")
    # load the data
    data = pd.read_csv('../data/credit_card_data.csv')
    return process(data)


def process(data):
    # drop irrelevant columns
    data = data.drop('CUST_ID', 1)
    data = data.drop('BALANCE_FREQUENCY', 1)
    data = data.drop('PURCHASES_FREQUENCY', 1)
    data = data.drop('ONEOFF_PURCHASES_FREQUENCY', 1)
    data = data.drop('PURCHASES_INSTALLMENTS_FREQUENCY', 1)
    data = data.drop('CASH_ADVANCE_FREQUENCY', 1)
    data = data.drop('PRC_FULL_PAYMENT', 1)


            # check if there are corrupted inputs in data
            # corruption = data.isna().sum()
            # print(corruption)

    # fill NA with median
            # data = data.apply(lambda x: x.fillna(x.mean()), axis=0)
    data = data.interpolate(method="linear")
            # double check corrupted inputs
            # corruption = data.isna().sum()
            # print(corruption)

    # deriving new KPI
            # Monthly Average Purchase
    data.insert(len(data.columns), "MONTHLY_AVG_PURCHASE", data['PURCHASES'] / data['TENURE'], True)
            # Monthly Cash Advance
    data.insert(len(data.columns), "MONTHLY_CASH_ADVANCE", data['CASH_ADVANCE'] / data['TENURE'], True)
            # Limit Usage Ratio
    data.insert(len(data.columns), "LIMIT_RATIO", data.apply(lambda x: x['BALANCE'] / x['CREDIT_LIMIT'], axis=1), True)
            # Payment: Min Payment
    data.insert(len(data.columns), "PAYMENT_MIN_RATIO", data.apply(lambda x: x['PAYMENTS'] / x['MINIMUM_PAYMENTS'], axis=1), True)

    get_insights(data)
    data = data.drop('PURCHASE_TYPE', 1)

    # outlier treatment - log transformation
            # data.plot(kind='box')
            # plt.show()
    data = data.applymap(lambda x: np.log(x + 1))
            # data.plot(kind='box')
            # plt.show()

    pd.set_option('display.max_columns', 25)

    # scale all values
    scalar = StandardScaler()
    data_scaled = scalar.fit_transform(data.values)
    data = pd.DataFrame(data_scaled, columns=data.columns)



    return data
