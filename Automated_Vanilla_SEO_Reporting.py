#!/usr/bin/env python3
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
    'CONSENT': 'YES+',
    'SID': 'Zwjkj5-9MAGqWLAvuB9t0IrjS5yOMWXod8T9pBKO_240vxGJUWBbkdgwO0HZUJUK2Izo7Q.',
    '__Secure-1PSID': 'Zwjkj5-9MAGqWLAvuB9t0IrjS5yOMWXod8T9pBKO_240vxGJ2q6TJcle-f9-RLQhAkqwSA.',
    '__Secure-3PSID': 'Zwjkj5-9MAGqWLAvuB9t0IrjS5yOMWXod8T9pBKO_240vxGJ8ND2oH_vGLPuC9wSavMnew.',
    'HSID': 'ANAdZFmGocDhxrkiE',
    'SSID': 'A92EIlMBd2nKLaq0j',
    'APISID': '6hMZHwrO-HLmkibI/AfEZlEgqqGKpaaAgx',
    'SAPISID': '3m80mJYy7fj3-oTk/AwhGxd5nNi7faYchZ',
    '__Secure-1PAPISID': '3m80mJYy7fj3-oTk/AwhGxd5nNi7faYchZ',
    '__Secure-3PAPISID': '3m80mJYy7fj3-oTk/AwhGxd5nNi7faYchZ',
    '1P_JAR': '2023-8-8-18',
    'AEC': 'Ad49MVGLWdHk7wU_E-4w0qT_RSbo0_Cw_OCP-SfiNvlNGOYH4m5Zlb0UNQ',
    'SOCS': 'CAISNQgCEitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjMwODE1LjA2X3AyGgJlbiAEGgYIgIyApwY',
    'DV': 'A5rYlOV_NhYoEBgRRJkc1dLhdnAqodiJV5getGLf6QEAAAA',
    'SIDCC': 'APoG2W8bViUAOtSwaywNcNFDXQN7WcJzcdFIPcCl8Sh-CCCGicQDMx3ammwVsOlGT-bv7r9Xogk',
    '__Secure-1PSIDCC': 'APoG2W_HzWlpvvDNhQjqXs3OX5ReZd6X_lNvT4G5mOAK474-qPya8Y7wJRW3qp_e--lVAtwVOsQ',
    '__Secure-3PSIDCC': 'APoG2W98vnGndsj51ptuDzmFbb7VG5hsmyFaFO3e1tc6cpVG5SyXpr85NuvpDAb8VVj3BFBohQ',
    'NID': '511=RkZqtocnL5Gb3U9sIO8j7FNJWF5KntvLfBGZRtCIxP_vTloIuRriAkJYpWj4FAnwZqnPr1Gi3Mny0VLBJiEZ5T0TmWiOhJMgRmjwuIpJJ3D6OCq8BLU0OWMbjg9BEwwyROIpNBSgSn8WRbalLxAcR9L92A09a1J09NXlhvyMCi6KjTQH6LACbKFEX29MwUY3F1B8kXgLD220pGXMioYLqXFNw4Tvb3omVSydmrWmq4n-HpODadezl4Fd5WFtMENvOK-MrzzEdo4',
    }

    headers = {
    'authority': 'www.google.com',
    'accept': '*/*',
    'accept-language': 'es-ES,es;q=0.9,en;q=0.8,fr;q=0.7,ca;q=0.6',
    'referer': 'https://www.google.com/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"115.0.5790.114"',
    'sec-ch-ua-full-version-list': '"Not/A)Brand";v="99.0.0.0", "Google Chrome";v="115.0.5790.114", "Chromium";v="115.0.5790.114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"10.15.7"',
    'sec-ch-ua-wow64': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'x-client-data': 'CI22yQEIprbJAQipncoBCKLdygEIlqHLAQiFk80BCIagzQEIk6vNAQjEsc0BCN20zQEI3L3NAQi7vs0BCODEzQEI78TNAQirxc0BCN3FzQEI9cXNAQiWyM0BGPamzQE=',
    } 
    
    params = {'q': '',
              'cp': 0,
              'client': 'desktop-gws-wiz-on-focus-serp',
              'xssi': 't',
              'gs_pcrt': 3,
              'hl': 'en-ES',
              'authuser': 0,
              'pq': '',
              'psi': 'GdDgZPrGB52Li-gP9tum-A8.1692454938338',
              'dpr': 2,
              'ofp': 'EAEyewoMCgp1bm8gb25saW5lChIKEHVubyBvcmdhbml6YXRpb24KCwoJdW5vIGNhcmRzCgsKCXVubyBydWxlcwoNCgt1bm8gd2Vic2l0ZQoQCg51bm8gdmlkZW8gZ2FtZQoKCgh1bm8gZnJlZQoOCgx1bm8gZG93bmxvYWQQRzJhChgKFklzIFVubyBhIFNwYW5pc2ggZ2FtZT8KJAoiSG93IGRvIHlvdSBwbGF5IHRoZSBjYXJkIGdhbWUgVW5vPwocChpXaGF0IGlzIHRoZSA3IHJ1bGUgaW4gVW5vPxDkAg',
              'start':''
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
    scraper.mentions('noticias barcelona', 1)
    scraper.parse_results()
    scraper.related_searches()
    #scraper.parse_rsearches_results()
 
#%%
#def clean_results(keyword):
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


#%% Visualize

#pie graph mentions percentage results
pie1 = px.pie(results,
              values = np.where(results['Mentions'],1,1),
              names = 'Mentions',
              height = 400,
              width = 400,
              color_discrete_sequence=['#e14b31','#005b96'],
              title = 'Mentions in results (%)')
pie1.update_layout(font_family='Lato')
plot(pie1)
#pie headers
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

#%%Html
with open('report.html','w') as report:
    report.write('<!DOCTYPE html>\
                 <html>\
                     <body>\
                         <h1>SEO Report</h1>\
                         <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'\
                         +plotly.offline.plot(rank_plot1, include_plotlyjs=False, output_type='div')+\
                         plotly.offline.plot(rank_plot2, include_plotlyjs=False, output_type='div')+\
                         plotly.offline.plot(total_plot, include_plotlyjs=False, output_type='div')+\
                         plotly.offline.plot(pie1, include_plotlyjs=False, output_type='div')+\
                         plotly.offline.plot(pie2, include_plotlyjs=False, output_type='div')+\
                     '</body>\
                 </html>')





fig = make_subplots(
    rows=2, cols=2,
    specs=[[{"type": "pie"}, {"type": "pie"}],
           [{"type": "pie"}, {"type": "pie"}]],
)

fig.add_trace(pie2.data[0],row=1,col=1)
fig.add_trace(pie1.data[0],row=1,col=2)
plot(fig)







                