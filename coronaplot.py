import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import pandas as pd
import os

def load_hopkis_data(path, sdate, edate, nbDaysbtw2dates=1):
    #sdate = date(2020,1,22)   # start date
    #edate = date(2021,3,13)   # end date
    date_modified=sdate
    dates=[sdate]

    while date_modified<edate:
        date_modified+=timedelta(days=nbDaysbtw2dates) 
        dates.append(date_modified)
    #print(dates) 

    basepath = "csse_covid_19_data/csse_covid_19_daily_reports"

    alldata = None
    for date in dates:
        filename = f"{date.month:02d}-{date.day:02d}-{date.year}.csv"
        fullpath = os.path.join(path, basepath, filename)

        with open(fullpath, "r") as file:
            header = file.readline()

        headerlist = header.split(",")
        country_index = None
        confirmed_index = None
        deaths_index = None
        recovered_index = None
        for i in range(len(headerlist)):
            if headerlist[i].replace("\n", "") in ["Country_Region", "Country/Region"]:
                country_index = i
            if headerlist[i].replace("\n", "") in ["Confirmed"]:
                confirmed_index = i
            if headerlist[i].replace("\n", "") in ["Deaths"]:
                deaths_index = i
            if headerlist[i].replace("\n", "") in ["Recovered"]:
                recovered_index = i
        #print(country_index, confirmed_index, deaths_index, recovered_index)

        #data = np.genfromtxt(fullpath, skip_header=1, delimiter=",", usecols=(country_index, confirmed_index, deaths_index, recovered_index))
        df = pd.read_csv(fullpath, sep=",", usecols=(country_index, confirmed_index, deaths_index, recovered_index), header=0,names=["country", "confirmed", "deaths", "recovered"])
        df = df.fillna(0)

        df = df.groupby("country").sum()
        df.index.name = "country"
        df.reset_index(inplace=True)

        #print(df)
        df["date"] = date
        if alldata is None:
            alldata = df
        else:
            alldata = pd.concat([alldata, df])
        #print(df)
        
    #print(alldata)
    return alldata

df = load_hopkis_data(r"C:\Users\milan\Downloads\COVID-19-master".replace("\\", "/"),date(2020,1,22),date(2021,3,13))
df.info()
#print(df)
selection = df[df["country"] == "Germany"]
print(selection["date"].to_numpy())
x = selection["date"].to_numpy()[1:]
y = selection["confirmed"].to_numpy()[1:]-selection["confirmed"].to_numpy()[:-1]
x_avg = x[6:]
y_avg = np.convolve(y, np.ones(7), 'valid')
plt.plot(x_avg, y_avg)
plt.show()