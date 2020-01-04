Trend in India, Pakistan and Philippine from Google Search Keywords
==================================================================

### Introduction:
Google is the most commonly used search engine in the world across all platforms, “with more than 5.4 billion searches each day and 78,881 searches in 1 second" (Google Search Statistics). Google Trend, also, offers an well-structured information within the limit of 1 - 30 Categories. There are top 10 popular keywords per each category, and lists on each year by each country from 2001 until now. The initial trends per each country are expected to see and capture each historical interests or big events over time.

The report tried to capture the global trends, however, Global dataset in Google trends does not support China and three Higher internet usage countries in Asia don’t use Google as a primary search engine (Internet Stats & Facts for 2019). Due to these reasons, the report decided to rather look up the regions that have a lower broadband penetration rate. The lower broadband penetration rate will be a great indicator to find out a less compatible market for the search engine, so it will lead to get more prominent results by using the Google search dataset to see those region’s overall trends.


### [Methodology](https://github.com/rimhoho/Google-Search-Trend-in-India_Pakistan-Philippine/blob/master/Clustering%20Data%20of%20Inia%2C%20Pakistan%20and%20Philippine%20in%20Google%20Trend%20.ipynb)
  * Choosing data `India, Pakistan, Philippine`
  * Collecting data `Selenium`
  * Cleaning data `Pandas and Regular Expression`
  * Preparing data for Clustering `CountVectorizer`
  * LDA model training and results `LatentDirichletAllocation`

### Findings:
`In overall, the keywords that go through India was Film, Pakistan got celebrities, and Pilippine had US culture, all of them can be classified by entertainment.`
In the early stage of searching in Google, India got the film and sports on their most of keywords, Pakistan had the celebrities the most, and Philippine got US films; songs; and dramas. These keywords are quite similar topics that might be under the entertainment classification. Since India and Pakistan both have the same film in 2018 (Tiger Zinda Hai: East Indian agent Tiger joins forces with Pakistani agent Zoya), it also can tell that they were gotten to each other with the common background and interest. Interestingly, Philippine has been favored in lots of American culture but not two other countries.

`Sports keyword is a key to describe these three countries’ hobbies and interests that have been played the same major sport event for a long time.`
Spatially, India and Pakistan have a lot of similarities in enjoying sports and holding sports events annually which are Football(FIFA World Cup), Cricket (IPL, Asia Cup), Kabaddi (Pro Kabaddi League) and Multi-sport Events (Asian Games, Commonwealth Games). These might cause of sharing the same culture in the past for a long time. On the other hand, Philippine have been only held in Football events (FIFA World Cup, Asian Games), but three countries all interested in watching the tennis games abroad such as Australian Open, Wimbledon.  

`Pilippine had already been interested in lots of different types of cultures, India has been gradually increased with a variety of topics in their interests, however, Pakistan still stick with their existing topics.`
India became to pay closer attention to education, politics and News. Pakistan, however, kept focusing on entertainment topics. Philippine is the most various types of interests but mostly focusing on the entertainment topics.
