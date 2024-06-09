"""This module contains the class for predicting bookings of new users"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from sklearn import preprocessing
import xgboost as xgb

class BookingPredictions:
    """Predict bookings of new users"""

    def __init__(self):
        self.train_data_file_name = "data_files/train_users.csv"

    def read_data(self, file_name: str) -> pd.DataFrame:
        """Reads csv and converts them to pandas dataframes"""
        df = pd.read_csv(file_name)
        return df

    def get_year_from_date(self, booking_date):
        """Extracts year number from date"""
        if booking_date == booking_date:
            return int(str(booking_date)[:4])
        return booking_date 

    def get_month_from_date(self, booking_date):
        """Extracts month number from date"""
        if booking_date == booking_date:
            return int(str(booking_date)[5:7])
        return booking_date

    def assign_gender(self, gender):
        """Assigns random gender to None records"""
        if gender not in ('MALE', 'FEMALE'):
            random_int = random.randrange(1, 10000)
            return 'MALE' if random_int % 2 == 0 else 'FEMALE'
        else:
            return gender

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """This method preprocesses the bookings data"""

        # fill nan values in date_first_booking with date_account_created
        df["date_first_booking"].fillna(
            df["date_account_created"], inplace=True)
        df = df.drop(
            ['date_account_created', 'timestamp_first_active'], axis=1)

        # Getting the year and month from date of first booking
        df['dfb_year'] = df["date_first_booking"].\
            apply(self.get_year_from_date)
        df['dfb_month'] = df['date_first_booking'].\
            apply(self.get_month_from_date)

        # replacing None values with median
        df['dfb_year'].fillna(df['dfb_year'].median(), inplace=True)
        df['dfb_month'].fillna(df['dfb_month'].median(), inplace=True)

        # getting the mid year flag from month
        df[['dfb_year', 'dfb_month']] = df[['dfb_year', 'dfb_month']].astype(int)
        df["mid_year"] = df["dfb_month"].apply(lambda x: 1 if x == 6 else 0)

        # Filling unassigned gender rows randomly with MALE or FEMALE
        df['gender'] = df['gender'].apply(self.assign_gender)
        df.drop(['gender'], axis=1, inplace=True)

        # Handling outlier values in age
        df["age"][df["age"] > 100] = np.NaN
        train_age_avg = df["age"].mean()
        train_age_std = df["age"].std()
        train_nan_age_size = df["age"].isnull().sum()

        # Filling outlier ages with proper values
        train_rand_age_list = np.random.randint(train_age_avg - train_age_std,
                                                train_age_avg + train_age_std,
                                                size= train_nan_age_size)
        df["age"][np.isnan(df["age"])] = train_rand_age_list
        df['age'] = df['age'].astype(int)
        df['age_range'] = pd.cut(df["age"], [0, 20, 40, 60, 80, 100])
        df.drop(['age_range'], axis=1, inplace=True)
        df.drop(['age'], axis=1, inplace=True)

        # Preprocessing for affliate columns
        count_first_affiliate = len(np.unique(
            df["first_affiliate_tracked"].value_counts()))
        count_nan_department_airbnb = df["first_affiliate_tracked"].isnull().sum()
        rand_1 = np.random.randint(0, count_first_affiliate, 
                                   size= count_nan_department_airbnb)
        range_departments_airbnb = df['first_affiliate_tracked'].\
            value_counts().index
        df["first_affiliate_tracked"][
            df["first_affiliate_tracked"] != df["first_affiliate_tracked"]] =\
                  range_departments_airbnb[rand_1]

        # signup_method
        df["signup_method"] = (df["signup_method"] == "basic").astype(int)
        # signup_flow
        df["signup_flow"] = (df["signup_flow"] == 3).astype(int)

        # language
        df["language"] = (df["language"] == 'en').astype(int)

        # affiliate_channel
        df["affiliate_channel"] = (
            df["affiliate_channel"] == 'direct').astype(int)

        # affiliate_provider
        df["affiliate_provider"] = (
            df["affiliate_provider"] == 'direct').astype(int)

        # Converting string columns to numeric via Encoding
        for column in df.columns:
            if column == "country_destination" or column == "id":
                continue
            if df[column].dtype == 'object':
                lbl = preprocessing.LabelEncoder()
                lbl.fit(np.unique(list(df[column].values)))
                df[column] = lbl.transform(list(df[column].values))

        return df

    def split_df(self, df, is_train: bool = True):
        """Splits dataframe into target and non-target columns"""
        if is_train:
            x_train = df.drop(["country_destination", "id"], axis=1)
        else:
            x_train = df.drop(["id"], axis=1)
        y_train = df["country_destination"] if is_train else None
        return x_train, y_train

    def train_xgb(self, x_train, y_train, x_test):
        """Predicts the destination country using XG Boost algo"""
        params = {"objective": "multi:softmax", "num_class": 12}
        t_train_xgb = xgb.DMatrix(x_train, y_train)
        x_test_xgb = xgb.DMatrix(x_test)

        gbm = xgb.train(params, t_train_xgb, 20)
        y_pred = gbm.predict(x_test_xgb)
        return y_pred

    def main(self, test_df):
        """Main function that calls all sub functions"""

        train_df = self.read_data(self.train_data_file_name)

        train_df = self.preprocess_data(train_df)
        test_df = self.preprocess_data(test_df)
        x_train, y_train = self.split_df(train_df)
        x_test, _ = self.split_df(test_df, is_train=False)

        country_num_dic = {'NDF': 0, 'US': 1, 'other': 2, 'FR': 3, 'IT': 4, 'GB': 5, \
                            'ES': 6, 'CA': 7, 'DE': 8, 'NL': 9, 'AU': 10, 'PT': 11}
        num_country_dic = {y: x for x, y in country_num_dic.items()}

        y_train = pd.Series(y_train).map(country_num_dic)

        # Run the XGb model
        y_pred = self.train_xgb(x_train, y_train, x_test)
        # convert type to integer
        y_pred = y_pred.astype(int)

        # change values back to original country symbols
        y_pred = pd.Series(y_pred).map(num_country_dic)

        country_df = pd.DataFrame({
            "id": test_df["id"],
            "country_destination": y_pred
        })
        return country_df

# obj = BookingPredictions()
# test_df = pd.read_csv("/home/FRACTAL/shrijan.choudhary/bookings/Analytics/kc-bookings/src/app/backend/apps/predict_booking/data_science/test_users.csv")
# obj.main(test_df)