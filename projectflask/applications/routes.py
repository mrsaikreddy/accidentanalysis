#DATA SCIENCE PROJECT 
#TEAM-1
#SAI KIRAN REDDY K
#KODAM KARTHIK
#KADAGALA PRANEETH
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file 
import plotly
import os
for dirname, _, filenames in os.walk('archive'):#generate the file names in a directory tree by walking the tree either top-down or bottom-up
    for filename in filenames:
        print(os.path.join(dirname, filename))
import matplotlib.pyplot as plt
import seaborn as sns #data visualisation for drawing attractive and informative statistical graphs
from flask import Flask
from flask import render_template
from flask import url_for
import plotly.graph_objs as go #reads graph internally and returns a fig
import plotly.express as px 
import json

sns.set()

app = Flask(__name__)
@app.route('/')
def index():
	
    accidents_raw = pd.read_csv('ds project/archive/only_road_accidents_data_month2.csv')

    accidents_raw.head()

     # Master Dataframe created to get dataframe metadata at one place.
     #data cleaning

    def master_dataframe(dataframe):
        df_metadata = pd.DataFrame({'Datatype': dataframe.dtypes,
                                    "Null Values": dataframe.isna().sum(),  
                                    "Null %": round(dataframe.isna().sum()/len(dataframe)*100, 2),
                                    "No: Of Unique Values": dataframe.nunique()})
        
        df_describe = dataframe.describe(include='all').T
        #description of data in dataframe
        df_metadata = df_metadata.join(df_describe)  
        #takes all items as an iteration and joins them in one string
        corr = dataframe.corr()
        fig, ax = plt.subplots(figsize = (15, 15))    
        sns.heatmap(ax=ax,
                    data=corr, 
                    annot=True,
                    cmap='flare')
       # plt.show()
       # The correlation coefficient is a statistical measure of the strength of a 
       # linear relationship between two variables. Its values can range from -1 to 1. A 
       # correlation coefficient of -1 describes a perfect negative, or inverse,
        return df_metadata

    master_dataframe(accidents_raw)


    accidents_raw['STATE/UT'].unique()
    #finds the unique values in series
    accidents_raw[(accidents_raw['STATE/UT'] == "Delhi Ut") | (accidents_raw['STATE/UT'] == "Delhi (Ut)")]


    # ### Updating the name of the UT as it is mentioned incorrect
    accidents_raw.at[139, 'STATE/UT'] = "Delhi (Ut)"


    # # BAR CHARTS

    #GRAPH-1
    #ACCIDENTS PER YEAR
    fig = px.bar(data_frame=accidents_raw, 
                x='YEAR', 
                y='TOTAL', 
                )

    fig.update_layout(title = {'x': 0.5})
    graph1JSON = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    #fig.show()


    #GRAPH-2
    #STATEWISE ACCIDENTS PER YEAR
    fig2 = px.bar(data_frame=accidents_raw, 
                x='YEAR', 
                y='TOTAL',
                color='STATE/UT', 
                barmode='stack',
                )

    fig2.update_layout(title = {'x': 0.5})
    graph2JSON = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
    

    #GRAPH-3
    #STATEWISE ACCIDENTS PER YEAR SIDE BY SIDE
    fig3= px.bar(data_frame=accidents_raw, 
                x='YEAR', 
                y='TOTAL',
                color='STATE/UT',
                barmode='group', 
                )

    fig3.update_layout(title = {'x': 0.5})
    graph3JSON = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
    #fig.show()

    #GRAPH-4
    #ACCIDENTS IN TAMIL NADU IN YEAR 2005 PER MONTH 
    tamil_nadu_2005 = accidents_raw[(accidents_raw['STATE/UT'] == "Tamil Nadu") & (accidents_raw['YEAR'] == 2005)].reset_index()
    tamil_nadu_2005.drop(columns=['STATE/UT', 'YEAR', 'TOTAL', 'index'], axis=1, inplace=True)
    tamil_nadu_2005 = tamil_nadu_2005.T.reset_index()
    tamil_nadu_2005.rename(columns={'index': 'Month', 0:'Accidents'}, inplace=True)


    fig4 = px.pie(data_frame=tamil_nadu_2005, 
                values='Accidents', 
                names='Month', 
                color_discrete_sequence=px.colors.sequential.Plasma, 
                 hole=0.2)

    fig4.update_layout(title = {'x': 0.5})
    graph4JSON = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
    #fig.show()
    
    #GRAPH-5
    #ACCIDENTS IN ANDHRA PRADESH IN YEAR 2005 PER MONTH 
    AP_2005 = accidents_raw[(accidents_raw['STATE/UT'] == "Andhra Pradesh") & (accidents_raw['YEAR'] == 2005)].reset_index()
    AP_2005.drop(columns=['STATE/UT', 'YEAR', 'TOTAL', 'index'], axis=1, inplace=True)
    AP_2005 = AP_2005.T.reset_index()
    AP_2005.rename(columns={'index': 'Month', 0:'Accidents'}, inplace=True)


    fig7 = px.pie(data_frame= AP_2005, 
                values='Accidents', 
                names='Month', 
                color_discrete_sequence=px.colors.sequential.Aggrnyl, 
                 hole=0.2)

    fig7.update_layout(title = {'x': 0.5})
    graph7JSON = json.dumps(fig7,cls=plotly.utils.PlotlyJSONEncoder)
    #fig.show()



    accidents_raw['STATE/UT'].unique()

    #GRAPH-6
    #ACCIDENTS PER YEAR BY COMPARING UNION TERRITORIES
    UTs = ["A & N Islands", "Chandigarh", "D & N Haveli", "Daman & Diu", "Delhi (Ut)", "Lakshadweep", "Puducherry"]
    accidents_UTs = accidents_raw[accidents_raw['STATE/UT'].isin(UTs)]
    accidents_UTs


    fig5 = px.bar(data_frame=accidents_UTs, 
                x='YEAR', 
                y='TOTAL',
                color='STATE/UT')
    fig5.update_layout(title = {'x': 0.5})
    graph5JSON = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
    #fig.show()
    df=accidents_raw
    fig8 = px.scatter_3d(df, 
                x='STATE/UT', 
                y='TOTAL', 
                z = 'YEAR',
                )
    fig8.update_layout(title = {'x': 0.5})
    graph8JSON = json.dumps(fig8,cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("index.html",graph1JSON = graph1JSON,graph2JSON = graph2JSON,graph3JSON = graph3JSON,graph4JSON = graph4JSON,graph5JSON = graph5JSON,graph7JSON = graph7JSON,graph8JSON = graph8JSON,)

if __name__ == '__main__':

	app.run(debug=False,host='0.0.0.0')




