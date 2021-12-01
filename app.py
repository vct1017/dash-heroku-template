import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

## Download and wrangle the ANES data
anes = pd.read_csv("https://raw.githubusercontent.com/vct1017/dash-heroku-template/master/gss2018.csv", low_memory=False)

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

myText = open(r'C:\Users\vincentterry\Documents\DS6001','w')


myString = 'Based on the website, https://americanprogress.org/article/quick-facts-gender-wage-gap/, it states that women on average earn just 82 cents for every dollar earned by men of all races. This statistic is quite troubling as it puts women in a serious situation of not earning what there potential should be. This article also states that the wage gap is even larger for women of color. Within the article it mentions that one of the reasons for the difference in years of experience between men and women would be that women are driven out of the workforce due to caregiving and other unpaid obligations. One last note that is disturbing from the article would be that over a 40-year career women will earn 407,760 dollars less than a man on average. Again, that is troubling as it makes known that there is a gender wage gap and this situation needs to be fixed.The General Social Survey (GSS), is a nationally representative survey of adults in the United States. The data collects on contemporary American society in order to monitor and explain trends in opinions, attitudes and behaviors. The data contains a standard core of demographic, behavioral, and attitudinal questions. Among some of the topics covered are civil liberties, crime and violence, intergroup tolerance, and morality. The data from the General Social Survey is high-quality and easily accessible for anyone to use. What I found to also be interesting would be that more than 130 papers have been published in the General Social Survey Methodological Reports series.'


myText.write(myString)
myText.close()

gss_bar = gss_clean.groupby('sex', sort=False).agg({'sex':'size',
                                     'income':'mean',
                                    'job_prestige':'mean',
                                    'socioeconomic_index':'mean',
                                    'education':'mean'})
gss_bar = gss_bar.rename({'sex':'Gender', 'income':'Annual Income','job_prestige':'Job Prestige', 'socioeconomic_index':'Socioeconomic Status', 'education':'Education'}, axis=1) #needed to avoid the same name as the index
gss_bar['Annual Income'] = round(gss_bar['Annual Income'],2)
gss_bar['Job Prestige'] = round(gss_bar['Job Prestige'],2)
gss_bar['Socioeconomic Status'] = round(gss_bar['Socioeconomic Status'],2)
gss_bar['Education'] = round(gss_bar['Education'],2)
gss_bar = gss_bar.reset_index()
#gss_bar['percent'] = round(100*gss_bar['Gender']/sum(gss_bar['Gender']),2)
gss_bar

table = ff.create_table(gss_bar)
table.show()

gss_plot_a = gss_clean.groupby(['sex', 'male_breadwinner']).size()
gss_plot_a = gss_plot_a.reset_index()
gss_plot_a = gss_plot_a.rename({0:'count'}, axis=1)
gss_plot_a

fig = px.bar(gss_plot_a, x='male_breadwinner', y='count', color='sex',
            labels={'sex':'Gender', 'count':'Feedback Count'},
            hover_data=['sex','male_breadwinner','count'],
            text='count',
            barmode='group')
fig.update_layout(showlegend=True)
fig.show()

fig_a = px.scatter(gss_clean, x='job_prestige', y='income',
                 trendline='ols',
                 color = 'sex', 
                 labels={'job_prestige':'Occupational Prestige', 
                        'income':'Annual Income'},
                 hover_data=['education', 'socioeconomic_index'])
#fig_a.update(layout=dict(title=dict(x=0.5)))
fig_a.layout.height=800
fig_a.layout.width=800
fig_a.show()
#height=600, width=600,

fig_b = px.box(gss_clean, x='income', y = 'sex', color = 'sex',
                   labels={'income':'Annual Income'},
                   title = 'Distribution of Income for Men vs. Women')
fig_b.update(layout=dict(title=dict(x=0.5)))
fig_b.update_layout(yaxis_visible=False)
fig_b.update_layout(showlegend=False)
fig_b.show()

fig_c = px.box(gss_clean, x='job_prestige', y = 'sex', color = 'sex',
                   labels={'income':'Annual Income'},
                   title = 'Distribution of Job Prestige for Men vs. Women')
fig_c.update(layout=dict(title=dict(x=0.5)))
fig_c.update_layout(yaxis_visible=False)
fig_c.update_layout(showlegend=False)
fig_c.show()

df = gss_clean[['income','sex','job_prestige']]
df

#cut_bins=[0,15,30,45,60,75,90]
#df['job_cat']=df['Prestige_Result'] = pd.cut(df['job_prestige'], cut_bins)
df['job_cat'] = pd.cut(df.job_prestige, bins=6, labels=["One", "Two", "Three", "Four", "Five", "Six"])

df = df.dropna()
df.head()

gss_plot = px.box(df, x='income', y = 'sex', color = 'sex',
facet_col='job_cat', facet_col_wrap=2,
labels={'income':'Annual Income', 'sex':''},
color_discrete_map = {'male':'blue', 'female':'red'},
                 category_orders = {"job_cat":["One", "Two", "Three", "Four", "Five", "Six"]})
gss_plot.layout.update(showlegend=False)
gss_plot.for_each_annotation(lambda a: a.update(text=a.text.replace("job_cat=", "Job Category: ")))
gss_plot.show()

#### Create App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div()
app.layout = html.Div(
    [
        html.H1("Exploring the 2019 General Social Survey"),
        
        dcc.Markdown(children=myString),
        
        html.H2("The Mean Income, Occupational Prestige, Socioeconomic Index, and Years of Education for Men and for Women"),
        
        dcc.Graph(figure=table),
        
        html.H2("The Number of Men and Women who Respond with Each Level of Agreement"),
        
        dcc.Graph(figure=fig),
        
        html.H2("Job Prestige versus Income"),
        
        dcc.Graph(figure=fig_a),
        
        html.Div([
            
            html.H2("Distribution of Income for Men vs. Women"),
            
            dcc.Graph(figure=fig_b)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H2("Distribution of Job Prestige for Men vs. Women"),
            
            dcc.Graph(figure=fig_c)
            
        ], style = {'width':'48%', 'float':'right'}),
        
        html.H2("Gender and Income: Job Prestige"),
        
        dcc.Graph(figure=gss_plot)
    ]
        
)
if __name__ == '__main__':
    app.run_server(debug=True, port=8053, host='0.0.0.0')
