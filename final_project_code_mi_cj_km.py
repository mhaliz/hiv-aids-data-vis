# -*- coding: utf-8 -*-
"""final_project_code_MI_CJ_KM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xdEWwt32RPoLGPapu8KKBzW6hdxpzkDw

# HIV/AIDS Dataset Analysis

### The purpose of this analysis is to understand the impacts and trends of the HIV/AIDS epidemic in the context of certain global measures aimed at ameliorating this epidemic.
Data downloaded from: 

*   HIV/AIDs: https://corgis-edu.github.io/corgis/csv/aids/
*   Global Dev: https://corgis-edu.github.io/corgis/csv/global_development/
*   GDP: https://data.worldbank.org/indicator/NY.GDP.PCAP.CD
*   Longitude/Latitude: https://simplemaps.com/resources/free-country-cities

Authors: Cole Steinmetz, Kory Melton, Michali Izhaky

Date: 5 October 2020

Contact: cjsteinmetz@dons.usfca.edu, kmelton@dons.usfca.edu, mizhaky@usfca.edu

Github usernames: Qstein, melt647, mhaliz
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Information about this dataset:
# https://corgis-edu.github.io/corgis/csv/aids/

# Download Data
folder = "/content/drive/My Drive/MSDS-group2/data/"
out_folder = "/content/drive/My Drive/MSDS-group2/output/"
aids_data_path = folder + "aids.csv"
cd_path = folder + "countries_of_the_world.csv"
global_dev = folder + "global_development.csv"
df = pd.read_csv(aids_data_path)
global_df = pd.read_csv(global_dev)
df.head()

# Define color scheme: 
RED='#ff1a75'
PURPLE = '#d24dff'
RED = '#ff1a75'
GREEN = '#009933'
DARK_GRAY = '#1a1a1a'
MEDIUM_GRAY = '#8c8c8c'
LIGHT_GRAY = '#cccccc'
LIGHT_GREEN = '#33ff77'
GREEN_GRAY = '#8aa893'

# Define style:
sns.set_style(style="white")

"""# Merge DFs to provide context for AIDS"""

aids_global_df = pd.merge(aids_df, global_df,
                          on=['Country', 'Year'])

# saved to a file
# name: '/content/drive/My Drive/MSDS-group2/data/aids_in_context.csv'

"""# Analyze impacts of the PMTCT in South Africa
### How do new HIV infection rates in children and females change following PMTCT implementation and subsequent acceleration?
This visualization compares new female infections with new child infections in the context of South Africa's plan to eliminate mother-to-child transmission (PMTCT).


source: https://www.who.int/bulletin/volumes/91/1/12-106807/en/

Plot made by Michali Izhaky
"""

# Create a new dataframe using just South Africa data,
# grouped by country and year,
# and takes the mean of New HIV infections in children and females
df2=df[(df.Country.isin(["South Africa"]))].groupby(by=["Country", "Year"], as_index=False)['Data.New HIV Infections.Children','Data.New HIV Infections.Female Adults'].mean()

# change float to integer type in a specific column
df2["Data.New HIV Infections.Female Adults"] = df2["Data.New HIV Infections.Female Adults"].astype(int)

# scale the data by 1000 so it looks nicer in the plot
df2['Data.New HIV Infections.Children'] = df2['Data.New HIV Infections.Children'].transform(lambda x: x/1000)
df2['Data.New HIV Infections.Female Adults'] = df2['Data.New HIV Infections.Female Adults'].transform(lambda x: x/1000)

# define figure and axis options, set figure size
fig, ax = plt.subplots(figsize=(11,7))

# plot first line showing new female infections by year
# and assign output to an axis object
ax1 = sns.lineplot(data=df2,
            x='Year',
            y='Data.New HIV Infections.Female Adults',
            linewidth=6,
            color=RED)
# plot second line showing new child infections by year
# and assign output to an axis object
ax2 = sns.lineplot(data=df2,
             x='Year',
             y='Data.New HIV Infections.Children',
             linewidth=6,
             color = PURPLE)

# set X tickmarks to equal the year
plt.xticks(df2['Year'])
# rotate these X tick labels 45 degrees
plt.xticks(rotation=45)

# add dotted vertical lines at the specified years
# each year signifies some milestone in the HIV/AIDS 
# Prevention of Mother to Child Transmission Programme (PMTCT)
# in South Africa
plt.vlines(x=2002, ymin=0, ymax=450, linestyles='dotted', colors='k')
plt.vlines(x=2004, ymin=0, ymax=350, linestyles='dotted', colors='k')
plt.vlines(x=2008, ymin=0, ymax=300, linestyles='dotted', colors=GREEN)

# give the plot a title
plt.title('New HIV Infections in Children Fall After \n Prevention of Mother to Child Transmission (PMTCT) \n Accelerated Plan is Implemented in South Africa \n \n',
          fontdict={'fontsize' : 20})

# declare same X axis used for both lines
ax2 = ax1.twinx()

# Clean up the appearance of the graph by removing spines
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.set_visible(False)

# define new labels: x label is not necessary to understand the x axis
ax1.set_xlabel('')
ax1.set_ylabel('New HIV Infections per 1000 People',
               fontsize = 14)

# Add text annotations to contextualize the dotted lines plotted above
ax1.text(2002, 450, "PMTCT first \n implemented", 
         ha='center', fontdict={'fontsize' : 9})
ax1.text(2004, 350, "Pregnant women \n eligible for \n Highly Active \n Antiretroviral \n Therapy \n (HAART)", ha='center',
         fontdict={'fontsize' : 9})
ax1.text(2008, 300, "PMTCT  \n Accelerated Plan \n Implemented", ha='center',
         fontdict={'fontsize' : 11,
                   'color': GREEN,
                   'weight' : 'semibold'})
ax1.text(2015.4, 200, "Women",
         fontdict={'fontsize' : 11,
                   'color': RED,
                   'weight': 'semibold'})
ax1.text(2015.4, 0.5, "Children",
         fontdict={'fontsize': 11,
                   'color' : PURPLE,
                   'weight' : 'semibold'})

# Save completed plot to the output directory
'''plt.savefig('/content/drive/My Drive/MSDS-group2/output/child_infections_PMTCT_MI.png',
            dpi=300,
            bbox_inches = 'tight')'''
plt.show()

"""# Analyze HIV Prevalence and Life Expectancy by African Region
### How do the different African regions (Northern, Southern, Eastern, Western, and Central) compare in terms of HIV prevalence vs life expectancy?

It is known that Sub-Saharan Africa is hit hardest by the AIDS epidemic. Conversely, Northern Africa is hit the least. This graph will visualize these differences, and include the other three African regions in context as well.

Plot made by Michali Izhaky
"""

# read in new csv dataset
df_kory = pd.read_csv('/content/drive/My Drive/MSDS-group2/data/aids_in_context.csv')

# look at these countries: 
# create dict to categorize regions in africa
groupings = {
  'North Africa': ['Algeria', 'Morocco', 'South Sudan', 'Sudan'],
  'East Africa': ['Kenya', 'Madagascar', 'Burundi', 'Djibouti', 'Eritrea',
                  'Malawi', 'Mozambique', 'Rwanda', 'Uganda', 'United Republic of Tanzania',
                  'Zambia', 'Somalia'],
  'Southern Africa': ['Lesotho', 'Botswana', 'Guyana', 'Namibia', 'South Africa', 'Swaziland',
                        'Zimbabwe'],
  'Central Africa': ['Angola', 'Cameroon', 'Central African Republic', 'Chad',
                      'Democratic Republic of the Congo', 'Equatorial Guinea',
                      'Gabon', 'Nicaragua'],
  'West Africa': ['Benin', 'Liberia', 'Burkina Faso', "C?te d'Ivoire", 'Cape Verde',
                  'Gambia','Ghana', 'Guinea', 'Mali', 'Mauritania', 'Niger', 'Nigeria',
                  'Senegal', 'Sierra Leone', 'Togo'],
  }

# coerce all values into a one dimensional list for easy subsetting
african_countries = [country for sublist in list(groupings.values()) for country in sublist]

# create a dataframe that includes only the African countries from the 
# dictionary created above, as well as only the columns specified below
d = df_kory[(df_kory.Country.isin(african_countries))].loc[:,["Country",
                                                                    "Year",
                                                    "Data.Health.Fertility Rate",
                                                    "Data.Health.Birth Rate",
                                                    "Data.Health.Life Expectancy at Birth, Female",
                                                    "Data.Health.Life Expectancy at Birth, Male",
                                                    "Data.Health.Life Expectancy at Birth, Total",
                                                    "Data.AIDS-Related Deaths.AIDS Orphans",
                                                    "Data.HIV Prevalence.Adults",
                                                    "Data.AIDS-Related Deaths.Children"]]
# A function to transform a country into its respective region, using the
# groupings dictionary
def transform_to_region(country):
  for key, val in groupings.items():
    if country in val:
      return key
# Apply the function to the Country column of my dataframe;
# create a new 'Region' column
d['Region'] = d.Country.apply(transform_to_region)

# Define new plot, figure size, and x axis will be shared
fig, ax = plt.subplots(1,2, sharex = True, figsize=(15,10))

# define color palette dict, heed preattentive attributes
plot_palette_dict = {'Central Africa' : MEDIUM_GRAY,
 'East Africa' : LIGHT_GRAY,
 'West Africa' : DARK_GRAY,
 'North Africa' : GREEN,
 'Southern Africa' : RED}
# Add title to plot
plt.title('Life Expectancy in Sub-Saharan Africa Decreases Significantly in Response to Rising HIV Prevalence \n',
          x=0,
          fontdict={
              'fontsize' : 20,
          })
# Define first axis object as a line plot showing life expectancy vs year,
# colored by region using the palette defined above
ax1 = sns.lineplot(data = d,
            x = "Year",
            y = "Data.Health.Life Expectancy at Birth, Total",
            hue = "Region",
            ci=None,
            ax=ax[0],
            legend=False,
            linewidth=3,
            palette = plot_palette_dict)

# Define the second axis object looking at HIV prevalence in adults by year
ax2 = sns.lineplot(data = d,
            x = "Year",
            y = "Data.HIV Prevalence.Adults",
            hue = "Region",
            ci=None,
            ax=ax[1],
            legend=False,
            linewidth=3,
            palette = plot_palette_dict)

# Clean up the appearance by getting rid of extra spines and labels
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.set_xlabel('')
ax2.set_xlabel('')

# Redefine y labels for both plots
ax1.set_ylabel('Life Expectancy at Birth',
               fontsize=14)
ax2.set_ylabel('HIV Prevalence (% of total population)',
               fontsize=14)

# specify which x ticks to show, set rotation to 45 degrees
plt.xticks([1990, 1992, 1994, 1996, 1998, 2000, 2002, 2004, 2006, 
            2008, 2010, 2012, 2014],
           rotation = 45)
# Set rotation for the ax1 object to 45 degrees as well
for tick in ax1.get_xticklabels():
    tick.set_rotation(45)

# Add line labels
ax2.text(2013.7, 20.2, 'Sub-Saharan Africa',
         ha='left',
         fontdict = {
             'fontsize' : 12,
             'color' : RED,
             'weight' : 'semibold'
         })
ax2.text(2013.6, 5.3, 'East Africa', ha='left',
         fontdict={
             'fontsize' : 12,
             'color' : LIGHT_GRAY,
             'weight' : 'regular'
         })
ax2.text(2013.54, 3.2, 'Central Africa',
         ha='left',
         fontdict = {
             'fontsize' : 12,
             'color' : MEDIUM_GRAY,
             'weight' : 'regular'
         })
ax2.text(2013.5, 1.3, 'West Africa',
         ha='left',
         fontdict = {
             'fontsize' : 12,
             'color' : DARK_GRAY,
             'weight' : 'regular'
         })
ax2.text(2013.5, 0, 'North Africa',
         ha='left',
         fontdict = {
             'fontsize' : 12,
             'color' : GREEN,
             'weight' : 'semibold'
         })
# Save image as png in output directory
'''plt.savefig('/content/drive/My Drive/MSDS-group2/output/life_expectancy_prevalence_MI.png',
            dpi=300,
            bbox_inches='tight')'''

"""# Compare women and children living with HIV by year in South Africa
### Contextualize the scatterplot by labeling which year different measures were enacted:

In July 2000, "UNAIDS, WHO, and other global health
groups announce a joint initiative with five major
pharmaceutical manufacturers to negotiate reduced
prices for HIV/AIDS drugs in developing countries" (via https://www.hiv.gov/sites/default/files/aidsgov-timeline.pdf).


In 2008, the Prevention of Mother to Child Transmission (PMTCT) was implemented.


In 2012, "The Joint United Nations Programme on HIV/AIDS reported that the following sixteen African nations in 2012 "ensure[d] that more than three-quarters of pregnant women living with HIV receive antiretroviral medicine to prevent transmission to their child" (via https://www.cdc.gov/mmwr/preview/mmwrhtml/su6004a11.htm)


From our previous analysis, we see that South Africa is hardest hit by HIV/AIDS. This scatterplot will contextualize how these three above measures impacted the rates of women and children living with HIV.


Plot made by Michali Izhaky/Kory
"""

# Make new dataframe containing only South Africa data
is_south_africa = df['Country'] == 'South Africa'
south_africa_df = df[is_south_africa]

# Scale data by 1000 for smaller y axis values
south_africa_df['Data.People Living with HIV.Children'] = df['Data.People Living with HIV.Children'].transform(lambda x: x/1000)

# Prepare lists of Year column and hex colors 
# to create a font dictionary that specifies the
# color of each label based on the year
l = list(south_africa_df.Year)
l1 = [DARK_GRAY] * 10
laa = [GREEN_GRAY] * 8
la = [LIGHT_GREEN] * 4
l2 = [GREEN] * 4
l3 = l1 + laa + la + l2
font_dict = dict(zip(l, l3))

# Set figure size
fig = plt.figure(figsize = (15,10))

# define custom color palette for scatterplot dot colors
customPalette = sns.color_palette("dark:salmon_r", as_cmap=True)

# Give plot a title
plt.title('Number of Children Living with HIV Decreases in South Africa After Providing \n Precautionary Prevention of Mother to Child Transmission Measures',
          fontsize = 20)

# Make scatterplot comparing HIV prevalence in young women with HIV prevalence
# in children; each dot represents a year
ax = sns.scatterplot(data=south_africa_df, 
                x='Data.HIV Prevalence.Young Women', 
                y='Data.People Living with HIV.Children', 
                hue='Year', 
                s=200,
                legend = False,
                palette = customPalette)
# Set axis labels appropriately
ax.set_ylabel('Children Living with HIV (thousands)', fontsize = 14)
ax.set_xlabel('Women Living with HIV', fontsize = 14)

# Use a for loop to label each dot in the scatterplot with the correct year
# and color each label according to the font_dict created earlier
count = 0
for line in range(0, south_africa_df.shape[0]):
 if count == 0:
   ax.text(list(south_africa_df.loc[: ,'Data.HIV Prevalence.Young Women'])[line] - 0.5,
         list(south_africa_df.loc[:, 'Data.People Living with HIV.Children'])[line] + 10, 
         list(south_africa_df.Year)[line],
         ha = 'left',
         fontdict = {'color' : list(font_dict.values())[line]}, size=14
         )
 else:
  ax.text(list(south_africa_df.loc[: ,'Data.HIV Prevalence.Young Women'])[line] + 0.2,
          list(south_africa_df.loc[:, 'Data.People Living with HIV.Children'])[line] - 3, 
          list(south_africa_df.Year)[line],
          ha = 'left',
          fontdict = {'color' : list(font_dict.values())[line]}, size=14
          )
 count += 1;
 # Add annotations to contextualize the data
 # and match the colors of the respective year labels
 ax.text(7, 250, '2012: \n Antiretrovirals \n distributed to \n 75% of \n pregnant women',
         color = GREEN, ha = 'left', fontweight='medium',
         size = 14)
 ax.text(8.3, 340, '2008: \n PMTCT \n implemented',
         color = LIGHT_GREEN, ha = 'left', size = 14)
 ax.text(17, 200, '2000: \n UNAIDS negotiated \n with 5 pharma companies \n to reduce antiretroviral \n drug prices for \n developing countries',
         color = GREEN_GRAY, ha = 'left', size = 12)
 
 sns.despine(top=True)
 
 # Save figure as png in output directory
 '''plt.savefig('/content/drive/My Drive/MSDS-group2/output/women_children_scatter_v2.png',
            dpi=300,
            bbox_inches='tight')'''

"""# Plot a heatmap of mortality rates for individuals with HIV by region

A countries wealth impacts the ability of its citizens to access healthcare including the expensive treatments for HIV. For this next section, we will combine HIV/AIDs data with GDP data and look at the differences between regions.
"""

# add regions to data above

groupings_all = {
  'North Africa': ['Algeria', 'Morocco', 'South Sudan', 'Sudan'],
  'East Africa': ['Kenya', 'Madagascar', 'Burundi', 'Djibouti', 'Eritrea',
                  'Malawi', 'Mozambique', 'Rwanda', 'Uganda', 'United Republic of Tanzania',
                  'Zambia', 'Somalia'],
  'Southern Africa': ['Lesotho', 'Botswana', 'Guyana', 'Namibia', 'South Africa', 'Swaziland',
                        'Zimbabwe'],
  'Central Africa': ['Angola', 'Cameroon', 'Central African Republic', 'Chad',
                      'Democratic Republic of the Congo', 'Equatorial Guinea',
                      'Gabon', 'Nicaragua'],
  'West Africa': ['Benin', 'Liberia', 'Burkina Faso', "C?te d'Ivoire", 'Cape Verde',
                  'Gambia','Ghana', 'Guinea', 'Mali', 'Mauritania', 'Niger', 'Nigeria',
                  'Senegal', 'Sierra Leone', 'Togo'],
  'Middle East': ['Azerbaijan', 'Iran (Islamic Republic of)', 'Egypt', 'Yemen'],
  'Australia': ['Australia'],
  'South America': ['Argentina', 'Belize', 'Bolivia (Plurinational State of)',
                    'Brazil', 'Colombia', 'Ecuador', 'Guatemala', 'Paraguay', 'Suriname',
                    'Uruguay', 'Venezuela (Bolivarian Republic of)'],
  'Central America and Mexico': ['El Salvador', 'Honduras', 'Panama', 'Peru', 'Mexico'],
  'Carribean': ['Bahamas', 'Cuba', 'Dominican Republic', 'Haiti', 'Jamaica', 
                'Trinidad and Tobago', 'Costa Rica'],
  'Europe': ['Belarus', 'Greece', 'Italy', 'Latvia', 'Georgia', 'Republic of Moldova',
              'Spain', 'Ukraine'],
  'Southeast Asia and Oceania': ['Bangladesh', 'Indonesia', 'Afghanistan', 'Malaysia', 'Myanmar', 'Nepal',
                  'Pakistan', 'Philippines', 'Sri Lanka', 'Thailand', 'Viet Nam', 'Papua New Guinea'],
  'Central Asia': ['Kazakhstan', 'Kyrgyzstan', 'Tajikistan', 'Uzbekistan', 'Mongolia']
  };

# new transform to region with all regions
def transform_to_region(country):
  for key, val in groupings_all.items():
    if country in val:
      return key

aids_global_df = df_kory.copy()
aids_df = df.copy()
aids_global_df['Region'] = aids_global_df.Country.apply(transform_to_region)
aids_df['Region'] = aids_df.Country.apply(transform_to_region)
aids_global_df

"""### Merge GDP data with aids in context. Then group the data by region. Finally sort the data by descending GDP."""

gdp_data_file = "/content/drive/My Drive/MSDS-group2/data/gdp_long.csv"
gdp_long = pd.read_csv(gdp_data_file, low_memory=False)
aids_by_gdp = pd.merge(aids_global_df, gdp_long, on=['Country','Year'])

regions = ['Australia', 'Carribean', 'South America', 'Europe',
           'Central Africa', 'East Africa', 'North Africa', 'Southern Africa', 
           'West Africa']

region_filtered_ag_df = aids_by_gdp[aids_by_gdp['Region'].isin(regions)]

region_filtered_ag_df
regions_by_gdp_df = region_filtered_ag_df.groupby(by='Region')\
  .mean()[['GDP']]\
  .sort_values('GDP', ascending=False)\
  .reset_index()

regions_by_gdp = regions_by_gdp_df.Region.to_list()
regions_by_gdp_df

"""## Plot Heatmap"""

import math
import numpy as np

# ao stands for aids only
heatmap_val_cols = ['Data.AIDS-Related Deaths.All Ages', 
              'Data.People Living with HIV.Adults'] 
grp_by = ['Region', 'Year']

ao_region_df_total = aids_df.groupby(by=grp_by).sum()
region_deaths_df = ao_region_df_total[heatmap_val_cols]

death_col = 'Data.AIDS-Related Deaths.All Ages'
norm_col = 'Data.People Living with HIV.Adults'

region_deaths_df['death_rate'] = region_deaths_df[death_col] / \
            (region_deaths_df[norm_col] + region_deaths_df[death_col] ) * 100

hm_2 = region_deaths_df['death_rate'].unstack(level=0)
regions = ['Australia', 'Carribean', 'South America', 'Europe',
           'Central Africa', 'East Africa', 'North Africa', 'Southern Africa', 
           'West Africa']

# # graph
# grid_kws = {"height_ratios": (0.9, .075), "hspace": .4}
# f, (ax, cbar_ax) = plt.subplots(2, gridspec_kw=grid_kws, figsize=(10,10))
# color maps:
#  YlOrBr
#  "YlGnBu"
hm_2_df = hm_2[regions_by_gdp].transpose()
c_scheme = "YlGnBu"
lw = 0.01

fig = plt.figure()
ax = sns.heatmap(hm_2_df, cmap=c_scheme, linewidth=lw, xticklabels=5)
#ax.set_title('Mortality Rate of People with HIV\nRegions are sorted by GDP\n')
ax.xaxis.tick_top()
ax.set(yticklabels=[])
ax.tick_params(left=False)
ax.set(ylabel=None)

'''fig.savefig(out_folder + "heatmap_death_per_HIV.png", bbox_inches="tight",
            dpi=300)'''

"""## Plot barchart for added context"""

sns.set_theme(style='white')

regions_by_gdp_df['high_gdp'] = regions_by_gdp_df['GDP'] > 5000

fig = plt.figure()
ax = sns.barplot(data=regions_by_gdp_df, x='GDP', y='Region',
            hue="high_gdp", dodge=False)
  
ax.get_legend().remove()
#ax.set_title("Australia and Europe have Significantly Highers Average GDPs")
sns.despine(top=True, bottom=True)
ax.set(yticklabels=[])
ax.tick_params(left=False)
ax.set(ylabel=None)

# fig.savefig(out_folder + "gdp_barplot.png", bbox_inches="tight", dpi=300)

"""# Get some total information if we want to put any summary info on our slidedeck"""

# Totals of important stats
## filter to africa

is_in_africa = lambda x: (x.find('Africa') != -1)
is_africa = aids_df['Region'].apply(is_in_africa)
africa_df = aids_df[is_africa]
africa_df.sum(axis=0)

"""# Make a scatterplot for a specified year

Use 2015 for the final plot, since this is the last year in the dataset
"""

## scatterplot for a year
year = 2015
is_in_year = africa_df['Year'] == year
yr_df = africa_df[is_in_year]

yr_df['deaths_thou'] = aids_df['Data.AIDS-Related Deaths.All Ages'] \
                                    / 1e3

## color palette
RED = '#ff1a75'
GREEN = '#009933'
DARK_GRAY = '#1a1a1a'
MEDIUM_GRAY = '#8c8c8c'
LIGHT_GRAY = '#cccccc'

# plot
fig = plt.figure()
ax = sns.scatterplot(data=yr_df, 
                x='Data.HIV Prevalence.Adults', 
                y='deaths_thou', 
                hue='Region', 
                palette = {
                'Central Africa' : MEDIUM_GRAY,
                'East Africa' : LIGHT_GRAY,
                'West Africa' : DARK_GRAY,
                'North Africa' : GREEN,
                'Southern Africa' : RED
                }, 
                 s=100, legend=False)

ax.set_xlabel("HIV Prevalence in Adults")
ax.set_ylabel("Deaths (Thousands)")
sns.despine(top=True)
# plt.legend(bbox_to_anchor =(1.50, 0.60))

# far top left is Nigeria
# far top right is South Africa
fig.savefig(out_folder + "hiv_scatter.png", bbox_inches="tight", dpi=300)

"""# Plot HIV Prevalence in Adults by GDP on World Map

Socioeconomics is the study of how economics affect social processes. Countries with low GDP may not have the resources to combat HIV within their communities. Looking at HIV prevalence by GDP over the course of three decades may give us some insight into the relationship between a countries wealth and its ability to give citizens access to healthcare.
"""

# To plot the data onto a world map, mpl_toolkits.basemap package needs to 
# be downloaded
# Installing the packages for Basemap
!apt-get install libgeos-3.5.0
!apt-get install libgeos-dev
!pip install https://github.com/matplotlib/basemap/archive/master.zip

"""# Using Basemap to generate a world map

For more information about this library, please goto the following links:

Installing Basemap (built from Matplotlib): 
https://matplotlib.org/basemap/users/installing.html

For examples using Basemap for plotting data: https://python-graph-gallery.com/315-a-world-map-of-surf-tweets/
"""

from mpl_toolkits.basemap import Basemap

# We will merge the aids data with GDP and Longitude/Latitude data
aids_context = pd.read_csv("/content/drive/My Drive/MSDS-group2/data/aids_in_context.csv", low_memory=False)
gdp_data = pd.read_csv("/content/drive/My Drive/MSDS-group2/data/global_gdp_by_year.csv", low_memory=False)
country_loc = pd.read_csv("/content/drive/My Drive/MSDS-group2/data/country_locations.csv", low_memory= False)

# First, get GDP data into long form
gdp_long = pd.wide_to_long(gdp_data,
                          stubnames='Year',
                          i= 'Country_Name',
                          j= 'Yr',
                          sep= ".")

gdp_long = gdp_long.rename(columns= {"Year": "gdp"})

#Merge aids and GDP datasets into one
aids_by_gdp = pd.merge(aids_context,gdp_long, on= ['Country','Year'])

# Merge aids/GDP and Longitude/Latitude datasets into one
aids_by_gdp = pd.merge(aids_by_gdp, country_loc, on= ['Country'])

# To compare data by decade, we need to create a new column in the dataset
# Create a decade column
# Credits go to Ken Simonds
def year_to_decade(year):
    year_str = str(year)
    return year_str[0:3] + '0s'

aids_by_gdp['Decade'] = aids_by_gdp.Year.transform(year_to_decade)

# To compare data by continent or region, I have reused code made by 
# Kory Melton. Below is a copy/paste of Kory's code above, for readability.
groupings = {
  'North Africa': ['Algeria', 'Morocco', 'South Sudan', 'Sudan'],
  'East Africa': ['Kenya', 'Madagascar', 'Burundi', 'Djibouti', 'Eritrea',
                  'Malawi', 'Mozambique', 'Rwanda', 'Uganda', 'United Republic of Tanzania',
                  'Zambia', 'Somalia'],
  'Southern Africa': ['Lesotho', 'Botswana', 'Guyana', 'Namibia', 'South Africa', 'Swaziland',
                        'Zimbabwe'],
  'Central Africa': ['Angola', 'Cameroon', 'Central African Republic', 'Chad',
                      'Democratic Republic of the Congo', 'Equatorial Guinea',
                      'Gabon', 'Nicaragua'],
  'West Africa': ['Benin', 'Liberia', 'Burkina Faso', "C?te d'Ivoire", 'Cape Verde',
                  'Gambia','Ghana', 'Guinea', 'Mali', 'Mauritania', 'Niger', 'Nigeria',
                  'Senegal', 'Sierra Leone', 'Togo'],
  'Middle East': ['Azerbaijan', 'Iran (Islamic Republic of)', 'Egypt', 'Yemen'],
  'Australia': ['Australia'],
  'South America': ['Argentina', 'Belize', 'Bolivia (Plurinational State of)',
                    'Brazil', 'Colombia', 'Ecuador', 'Guatemala', 'Paraguay', 'Suriname',
                    'Uruguay', 'Venezuela (Bolivarian Republic of)'],
  'Central America and Mexico': ['El Salvador', 'Honduras', 'Panama', 'Peru', 'Mexico'],
  'Carribean': ['Bahamas', 'Cuba', 'Dominican Republic', 'Haiti', 'Jamaica', 
                'Trinidad and Tobago', 'Costa Rica'],
  'Europe': ['Belarus', 'Greece', 'Italy', 'Latvia', 'Georgia', 'Republic of Moldova',
              'Spain', 'Ukraine'],
  'Southeast Asia and Oceania': ['Bangladesh', 'Indonesia', 'Afghanistan', 'Malaysia', 'Myanmar', 'Nepal',
                  'Pakistan', 'Philippines', 'Sri Lanka', 'Thailand', 'Viet Nam', 'Papua New Guinea'],
  'Central Asia': ['Kazakhstan', 'Kyrgyzstan', 'Tajikistan', 'Uzbekistan', 'Mongolia']
  };

def transform_to_region(country):
  for key, val in groupings.items():
    if country in val:
      return key

# Add a Region column to the dataset.
aids_by_gdp['Region'] = aids_by_gdp.Country.apply(transform_to_region)

"""# Creating the World Map and Plotting Data 

The next section is for subsetting the aids/GDP data to only African countries and plotting the HIV prevalence and GDP onto the world map.
"""

# Subset aids_by_gdp to only African Countries
is_in_africa = lambda x: (x.find('Africa') != -1)
is_africa = aids_by_gdp['Region'].apply(is_in_africa)
data = aids_by_gdp[is_africa]

data = data.groupby(by=['Decade','Country']).mean().reset_index()

# Create a new column that ranks GDP values from low to high.
# This column will be used later to visualize GDP by color.
data['label_color'] = data.GDP.rank(ascending=True)

# Sanity check
#data = data.sort_values(by='GDP', ascending=True)

# Drop NaN values - Some countries are missing HIV Prevalence data
data = data.dropna(axis=0)

# World Map & Plotting code
# Code was turned into a Function so that I could easily generate multiple 
# graphs depending on which decade I wanted. 
# Credit to Kory for helping me get this code working and making the 
# visualization look amazing.

def world_map_decade(decade):
  data = aids_by_gdp[is_africa]

  data = data.groupby(by=['Decade','Country']).mean().reset_index()

  data['label_color'] = data.GDP.rank(ascending=True)

  # Drop NaN values - Again
  data = data.dropna(axis=0)

  # Subset data to the chosen decade
  data = data[data.Decade == decade]
  
  # Set the dimension of the figure
  my_dpi= 96
  plt.figure(figsize=(2600/my_dpi, 1800/my_dpi), dpi=my_dpi)

  # Make the background map
  m= Basemap(llcrnrlon=-180, llcrnrlat=-65,urcrnrlon=180,urcrnrlat=80)
  m= Basemap()

  # cool alterative map backgroups - Seriously Check them out. 
  #m.shadedrelief()
  #m.bluemarble() 
  
  # Coloring of basic map
  m.drawmapboundary(fill_color='#DEF5FF', linewidth=0)
  m.fillcontinents(color=LIGHT_GRAY, alpha=0.3)
  m.drawcoastlines(linewidth=0.5, color="black")
  m.drawcountries(color='black')

  # Variables 
  # GDP is visualized as the fill color of each circle
  # HIV Prevalence is visualized as the circle's diameter 
  # radius_scale reduces the circle's diameter so that circles are not 
  # overlapping one another.
  col_color = 'GDP'
  col_radius = 'Data.HIV Prevalence.Adults'
  radius_scale = 60 

  # Create color scale for use in cmap
  pal = "rocket" 
  cmap= sns.color_palette(pal, as_cmap=True)

  # Add a point per position
  m.scatter(data['Longitude'],
            data['Latitude'],
            s= data[col_radius]*radius_scale,
            alpha= 1,
            c= data['label_color'],
            cmap= cmap,
            edgecolor= 'black',
            linewidth= 1)

  # Add legend
  m.colorbar(location= 'right', size = '1%', pad= '1%')

  # Save as png
  plt.savefig('/content/drive/My Drive/MSDS-group2/output/aids_preva_by_gdp_Bubble_map' + '_' + decade + '.png', bbox_inches='tight')
  plt.show

# Call world map decade function 
world_map_decade("1990s")

"""# Visualize HIV Prevalence by GDP, comparing Genders

To gain deeper insite into the socioeconomics of HIV in Africa, lets create a dot plot to compare which gender is more affected by low GDP
"""

# Split data by Sex, plus Children
data_two = aids_by_gdp.copy()
data_two['hiv_in_male'] = data_two['Data.People Living with HIV.Male Adults']/data_two['Data.People Living with HIV.Total']
data_two['hiv_in_female'] = data_two['Data.People Living with HIV.Female Adults']/data_two['Data.People Living with HIV.Total']
data_two['hiv_in_children'] = data_two['Data.People Living with HIV.Children']/data_two['Data.People Living with HIV.Total']

# Again reusing a part of Kory's code to quickly subset out the aid's data
# to only African countries. 
is_in_africa = lambda x: (x.find('Africa') != -1)
is_africa = data_two['Region'].apply(is_in_africa)
africa_df = data_two[is_africa]

# For this next graph we want Gender as a single column
# I needed to "merge" the two columns 'hiv_in_male' and 'hiv_in_female' into
# one.
keys = ['Country', 'GDP', 'Year', 'Gender', 'HIV_rate', 'Decade']
africa_sex_df = pd.DataFrame(columns= keys)

for index, row in africa_df.iterrows():
  vals = []
  vals.append(row.Country)
  vals.append(row.GDP)
  vals.append(row.Year)
  vals.append('Female')
  vals.append(row.hiv_in_female)
  vals.append(row.Decade)
  
  vals_m = []
  vals_m.append(row.Country)
  vals_m.append(row.GDP)
  vals_m.append(row.Year)
  vals_m.append('Male')
  vals_m.append(row.hiv_in_male)
  vals_m.append(row.Decade)

  vals_c = []
  vals_c.append(row.Country)
  vals_c.append(row.GDP)
  vals_c.append(row.Year)
  vals_c.append('Child')
  vals_c.append(row.hiv_in_male)
  vals_c.append(row.Decade)

  female_dict = dict(zip(keys, vals))
  male_dict = dict(zip(keys, vals_m))
  child_dict = dict(zip(keys, vals_c))
  
  africa_sex_df = africa_sex_df.append(female_dict, ignore_index=True)
  africa_sex_df = africa_sex_df.append(male_dict, ignore_index=True)
  africa_sex_df = africa_sex_df.append(child_dict, ignore_index=True)

# Sanity Check
africa_sex_df

"""# Creating a Seaborn Dot Plot

Kory found an interesting type of graph called a Dot Plot. For more information about Seaborn's Dot Plot, please follow this link: https://seaborn.pydata.org/examples/pairgrid_dotplot.html
"""

# Graph Num. 2 Dot Plot
columns = ['Country', 'GDP', 'hiv_in_male', 'hiv_in_female', 'hiv_in_children']
data_plot = africa_df[columns]
data_plot = data_plot.groupby(by= ['Country']).mean().reset_index()
data_plot = data_plot.sort_values(by= ['GDP'], ascending=False)

# I will create a vertical line down the x-axis that is the average M/F/Child
# living with HIV.
mean_male = data_plot['hiv_in_male'].mean()
mean_female = data_plot['hiv_in_female'].mean()
mean_child = data_plot['hiv_in_children'].mean()

print(mean_male)
print(mean_female)
print(mean_child)

# Dot Plot Code
sns.set_theme(style= "darkgrid")
g = sns.PairGrid(data_plot,
                     x_vars= data_plot.columns[1:5],
                     y_vars= "Country",
                     height= 10, 
                     aspect= .25)
g.map(sns.stripplot,
      size= 10,
      orient="h",
      palette="flare",
      linewidth= 1,
      edgecolor="w")

titles = ["Country", "GDP", "HIV_Male", "HIV_Female", "HIV_Children"]

for ax, title in zip(g.axes.flat, titles):
  # Set a different title for each axes
  if title == 'GDP':
    ax.set_xlim(0.25, 0.7)
    ax.vlines(x= mean_male, ymin= 0, ymax= 37, color= "red")
    ax.vlines(x= 0.5, ymin= 0, ymax= 37, color= "black")

  elif title == 'HIV_Male':
    ax.set_xlim(0.25,0.7)
    ax.vlines(x= mean_female, ymin= 0, ymax= 37, color= "red")
    ax.vlines(x= 0.5, ymin= 0, ymax= 37, color= "black")

  elif title == 'HIV_Female':
    ax.set_xlim(0.01, 0.13)
    ax.vlines(x= mean_child, ymin= 0, ymax= 37, color= "red")

  # Make the grid horizontal instead of vertical
  ax.xaxis.grid(False)
  ax.yaxis.grid(True)

sns.despine(left=True, bottom=True)
g.savefig('/content/drive/My Drive/MSDS-group2/output/DotPlot.png')