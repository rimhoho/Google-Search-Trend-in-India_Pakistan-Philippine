# Project 2- Google Trends

Dataset: https://trends.google.com/trends/yis/2018/US/

Visualization Inspiration: https://www.d3-graph-gallery.com/lollipop.html

Description: 

For Project 2, we want to use Selenium to scrap data from the Google Trends page and pull images from Google Images using
Google's API and put it in a MongoDB database. 

We plan to keep and utilize each of the categories of the trends and the 10 results in each category, and we also want to 
try and scrape multiple years of Google trends.

Once we have scraped and cleaned our html data and stored it in the database, we will then use it in an interactive D3 js 
lollipop visualization. 

There will be 2 filters on the webpage: one for the year and one for the category of the trend. 

Each of the lollipop circles will be interactive with a mouseover popup that will have the name of the trend and a google 
image of the trend with the top related search query to the trend.