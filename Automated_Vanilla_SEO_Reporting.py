# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 23:53:14 2023

@author: joanmiquel
"""
#%%   Libraries

import numpy as np
import pandas as pd
from plotly import express as px
import plotly.offline
from plotly.offline import plot
from plotly.subplots import make_subplots
import requests as re
from bs4 import BeautifulSoup
from parsel import Selector

#%% Define Scraper

class google_scraper:
    cookies = {
        #Add cookies from browser
    }

    headers = {
        #Add headers from browser
    } 
    
    params = {'q': '',
              'pq': '',
              'start':''
              #Add remaining parameters from browser
              }
    base_url = 'https://www.google.com/search'
    
    def mentions (self,query:str,page:int):
        self.params['q'] = query
        self.params['pq'] = query
        self.params['start'] = f'{10*(page-1)}' if page > 0  else 0
        self.response = re.get(self.base_url, headers = self.headers, params = self.params, cookies = self.cookies)
        self.selector = Selector(self.response.text)

    def related_searches (self):
        related_search = self.selector.xpath('//*[@id="bres"]/div/div/div/div/div/div/div/div')
        
        for i in related_search:
            r_search = i.get()
            r_search = BeautifulSoup(r_search,'html.parser')
            related_searches.append(r_search.get_text())   
    
    def parse_results (self):
        selector = Selector(self.response.text)
        for i in selector.xpath('//*[@class="MjjYud"]/div/div'): 
            data = i.get()
            data = BeautifulSoup(data,'html.parser')
            header = data.find('h3')
            
            if header is not None:
                header = header.get_text()
                headers.loc[len(headers)]={'Headers':header,'Query':self.params['q']}
                data.h3.decompose()
                result = data.get_text()
                results.loc[len(results)]={'Results':result,'Query':self.params['q']}
  
    def parse_rsearches_results (self):
        for i in related_searches:
            scraper.mentions(i, 1)
            scraper.parse_results()


#%% Execute scraping
if __name__ == '__main__':
    
    results = pd.DataFrame(columns =['Results','Query'])
    headers = pd.DataFrame( columns =['Headers','Query'])
    related_searches = list()
    
    scraper = google_scraper()
    scraper.mentions('La Vanguardia', 1)
    scraper.parse_results()
    scraper.related_searches()
    #Enable next step to repeat the search process for the related keywords suggested by Google
    #scraper.parse_rsearches_results()
 
#%% Results processing

results['Mentions'] = np.where(results['Results'].str.contains('Vanguardia'),'La Vanguardia','Other')
headers['Mentions'] = np.where(headers['Headers'].str.contains('Vanguardia'),'La Vanguardia','Other')
results['Rank'] = results.groupby('Query').cumcount()+1
headers['Rank'] = headers.groupby('Query').cumcount()+1

resmelt=pd.melt(headers,['Query','Mentions','Rank'],['Headers'])
headmelt=pd.melt(results,['Query','Mentions','Rank'],['Results'])

plot_df=pd.merge(resmelt,headmelt,on=['Query','Rank'],suffixes=('_Headers', '_Results'))
plot_df=pd.melt(plot_df,['Query','Rank'],['value_Headers','value_Results'])

plot_df['Mentions'] = np.where(plot_df['value'].str.contains('Vanguardia'),'La Vanguardia','Other')
plot_df['Mentions_count'] = np.where(plot_df['Mentions']=='La Vanguardia',1,0)


#%% Visualize results with interactive graphs

#Pie graph mentions percentage results
pie1 = px.pie(results,
              values = np.where(results['Mentions'],1,1),
              names = 'Mentions',
              height = 400,
              width = 400,
              color_discrete_sequence=['#e14b31','#005b96'],
              title = 'Mentions in results (%)')
pie1.update_layout(font_family='Lato')
plot(pie1)

#Pie headers
pie2 = px.pie(headers,
              values = np.where(headers['Headers'],1,1),
              names = 'Mentions',
              height = 400,
              width = 400,
              color_discrete_sequence=['#e14b31','#005b96'],
              title = 'Mentions in headers (%)')
pie2.update_layout(font_family='Lato')
plot(pie2)

#Rank per query
rank_plot1 = px.strip(plot_df[(plot_df['Rank']>0)&(plot_df['Mentions']=='La Vanguardia')],
                      x='Query',
                      y='Rank',
                      color ='variable',
                      color_discrete_sequence=['#1984c5','#e14b31']
                      )

rank_plot1.update_traces(marker={'size': 10})
rank_plot1.update_yaxes(autorange="reversed", row=1, col=1)
rank_plot1.update_layout(title = 'Rank by Query',
                         xaxis_title='',
                         yaxis_title='Rank',
                         legend_title='',
                         template = 'seaborn',
                         font_family="Lato")

plot(rank_plot1)

#Count of ranks 1,2 and 3 for all queries
rank_plot2 = px.bar(plot_df[(plot_df['Rank']>0)&(plot_df['Rank']<=3)&(plot_df['Mentions']=='La Vanguardia')].groupby(['Rank','variable'],as_index=False).count(),
              x='Rank',
              y='Mentions',
              color = 'variable',
              barmode = 'group',
              height = 600,
              width = 700,
              color_discrete_sequence=['#1984c5','#e14b31'])
rank_plot2.update_traces(width=0.25)
rank_plot2.update_yaxes({'tickformat': ',d'})
rank_plot2.update_yaxes(nticks=int(plot_df[(plot_df['Rank']>0)&(plot_df['Rank']<=3)&(plot_df['Mentions']=='La Vanguardia')].groupby(['Rank','variable'],as_index=False).count().max()['Mentions_count'])+1) 
rank_plot2.update_layout(title = 'Number of Mentions by Rank',
                         xaxis_title='Rank',
                         yaxis_title='Mentions',
                         legend_title='',
                         template = 'seaborn',
                         font_family="Lato")

plot(rank_plot2)

# Total mentions count bar graph horizontal
total_plot = px.bar(plot_df.groupby('variable',as_index=False).sum(),
                    x='Mentions_count',
                    y='variable',
                    color='variable',
                    color_discrete_sequence=['#1984c5','#e14b31'])
total_plot.update_traces(width=0.1)
total_plot.update_layout(title = 'Total Mentions',
                         xaxis_title='Mentions',
                         yaxis={'showticklabels':False,
                                'title':''},
                         legend={'title':''},
                         template = 'seaborn',
                         font_family='Lato')

plot(total_plot)

#%% Create sample HTML document with interactive graphs
with open('report.html','w') as report:
    report.write('''
                 
<!DOCTYPE html>
 <html lang="en">
 <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>SEO Report</title>
     <style>
         @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
         body {
             font-family: 'Roboto', sans-serif;
             margin: 0;
             padding: 20px;
             background-color: #f9f9f9;
         }
         .container {
             max-width: 800px;
             margin: 0 auto;
             background-color: #fff;
             padding: 50px;
             border-radius: 8px;
             box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
         }
         h1 {
             text-align: center;
             color: #333;
         }
         .graph {
             margin-bottom: 40px;
             max-width: 600px;
             margin-left: auto; 
             margin-right: auto; 
         }
         p {
            line-height: 1.6;
            margin-bottom: 20px;
            text-align: justify; 
        }
     </style>
 </head>
 <body>
     <div class="container">
      <h1>SEO Report</h1>
      <h2>Sample HTML Document</h2>
      '''
      '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
                         +plotly.offline.plot(rank_plot1, include_plotlyjs=False, output_type='div')+
                         '<h3>Lorem Ipsum</h2>\
                         <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus vitae \
                          aliquam arcu. Ut vitae ultrices odio. Curabitur facilisis turpis sit amet neque\
                          suscipit consequat. Integer et eleifend velit. Vivamus consequat tempor elit, nec\
                          venenatis ipsum laoreet eget. Fusce vehicula neque at diam volutpat, non euismod\
                          lorem cursus.</p>'
      '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
                         +plotly.offline.plot(rank_plot2, include_plotlyjs=False, output_type='div')+
                         '<h3>Lorem Ipsum</h2>\
                          <p>Nullam malesuada orci ac bibendum eleifend. Pellentesque habitant morbi\
                          tristique senectus et netus et malesuada fames ac turpis egestas. Nunc at\
                          malesuada lorem. Nam fringilla mi sit amet felis ultricies, id facilisis eros\
                          vulputate. Fusce nec nisi sem. Duis aliquam, nisl at tristique lobortis, magna\
                          purus sollicitudin eros, in faucibus mauris justo sit amet sem.</p>\
     </div>\
 </body>\
 </html>'
                 )






                
