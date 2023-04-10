from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from . import db
import pandas as pd
import numpy as np
import calendar
import pickle
from xgboost import XGBRegressor

model = pickle.load(open(r'C:\Users\Tausif shaikh\Downloads\flask_authentication\project\xgb_reg.sav', 'rb'))

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/predict' ,methods=['GET', 'POST'])
@login_required
def predict():
    data=pd.read_csv(r"C:\Users\Tausif shaikh\Downloads\flask_authentication\project\dashapp\walmart_clean_data.csv")
    stores=np.sort(data['Store'].unique())
    depts=np.sort(data['Dept'].unique())
    month_name=calendar.month_name[1:]
    month_no=[1,2,3,4,5,6,7,8,9,10,11,12]
    type=np.sort(data["Type"].unique())
    holidays=["Yes","No"]

    if request.method == 'POST':
        Type_A=0
        Type_B=0
        Type_C=0
        IsHoliday_False=0
        IsHoliday_True=0
        store=float(request.form.get('store'))
        dept=float(request.form.get('dept'))
        temp=float(request.form.get('temp'))
        fuilPrice=float(request.form.get('fuilPrice'))
        markd1=float(request.form.get('markd1'))
        markd2=float(request.form.get('markd2'))
        markd3=float(request.form.get('markd3'))
        markd4=float(request.form.get('markd4'))
        markd5=float(request.form.get('markd5'))
        cpi=float(request.form.get('cpi'))
        unemployment=float(request.form.get('unemployment'))
        size=float(request.form.get('size'))
        month=float(request.form.get('month'))
        year=float(request.form.get('year'))
        stype=request.form.get('type')
        if stype=="A":
            Type_A=1.0
        elif stype=="B":
            Type_B=1.0
        else:
            Type_C=1.0
        holiday=request.form.get('holiday')
        if holiday=="Yes":
            IsHoliday_True=1.0
        elif holiday=="No":
            IsHoliday_False=1.0
        
        values=[int(store),int(dept),int(temp),int(fuilPrice),int(markd1),int(markd2),
                int(markd3),int(markd4),int(markd5),int(cpi),int(unemployment),int(size),
                int(month),int(year),stype,holiday]
        
        data=pd.DataFrame({"Store":store,"Dept":dept,"Temperature":temp,"Fuel_Price":fuilPrice,
                  "MarkDown1":markd1,"MarkDown2":markd2,"MarkDown3":markd3,"MarkDown4":markd4,
                  "MarkDown5":markd5,"CPI":cpi,"Unemployment":unemployment,"Size":size,"month":month,
                  "year":year,"Type_A":Type_A,"Type_B":Type_B,"Type_C":Type_C,"IsHoliday_False":IsHoliday_False,
                  "IsHoliday_True":IsHoliday_True},index=[0])
        
        standard_scaler = StandardScaler()
        feature_cols = ['Temperature', 'Fuel_Price', 'MarkDown1','MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5', 'CPI', 'Unemployment', 'Size']
        transformed_features = standard_scaler.fit_transform(data[feature_cols])
        data[feature_cols] = transformed_features
        preds = model.predict(data)[0]
        print(preds)
        return render_template('prediction_result.html', values=values, result=preds,stores=stores,dept=depts,month_name=month_name,month_no=month_no, type=type, holiday=holidays)


    
    return render_template('prediction.html', stores=stores,dept=depts,month_name=month_name,month_no=month_no, type=type, holiday=holidays)