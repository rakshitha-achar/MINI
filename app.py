from flask import Flask, render_template, request, redirect
from utils.db import db
from models.data import *
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(_name_)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db.init_app(flask_app)


@flask_app.route('/')
def index():
    data = Business.query.all()
    return render_template('index.html', content=data)


@flask_app.route('/help')
def help():
    return render_template('help.html')


@flask_app.route('/add_data')
def add_data():
    return render_template('add_data.html')


with flask_app.app_context():
    db.create_all()


@flask_app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    print(f"form_data: {form_data}")

    user_id = form_data.get('id')
    age = form_data.get('age')
    gender = form_data.get('gender')
    UserBehaviorClass = form_data.get('UserBehaviorClass')

    mobile_id = form_data.get('mobile_id')
    DeviceModel = form_data.get('DeviceModel')
    OperatingSystem = form_data.get('OperatingSystem')
    AppUsageTime = form_data.get('AppUsageTime')
    BatteryDrain = form_data.get('BatteryDrain')
    ScreenOnTime_hours_per_day = form_data.get('ScreenOnTime_hours_per_day')
    NumberofAppsInstalled = form_data.get('NumberofAppsInstalled')
    DataUsage_MB_per_day = form_data.get('DataUsage_MB_per_day')

    user = User.query.filter_by(id=user_id).first()
    if not user:
        user = User(id=user_id, age=age, gender=gender, UserBehaviorClass=UserBehaviorClass)
        db.session.add(user)
        db.session.commit()

    data = Mobile(DeviceModel=DeviceModel, mobile_id=mobile_id, OperatingSystem=OperatingSystem,
                  BatteryDrain=BatteryDrain, AppUsageTime=AppUsageTime,
                  ScreenOnTime_hours_per_day=ScreenOnTime_hours_per_day,
                  NumberofAppsInstalled=NumberofAppsInstalled, DataUsage_MB_per_day=DataUsage_MB_per_day)
    db.session.add(data)
    db.session.commit()

    print("submitted successfully")
    return redirect('/')


if _name_ == '_main_':
    flask_app.run(host='127.0.0.1', port=8005,debug=True)
