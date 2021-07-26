
  
  
 # Halo 5 - Recommendations for Improved Player Experience through Data Visualization and Machine Learning

**Author**: [Johnny Dryman](mailto:johnnydryman@gmail.com)

## What is Halo 5?

**Halo 5: Guardians** is a 2015 first-person shooter video game developed by 343 Industries and published by Microsoft Studios for the Xbox One.  One of the most popular features of Halo 5 is its Arena multiplayer mode, where two teams of 4 players compete in a variety of game modes.  


# Introduction

We all had our various ways of getting through the 2020 lockdown - something to keep in touch with people and feel sane.  For me and my friends, we got through it with Halo 5 - specifically their 'Super Fiesta' game mode.  

While we had all played Halo 5 for a short period when it first launched in 2015, we hadn't really touched it since.  Before I even started the data science program at Flatiron, I thought it must somehow be possible to get more data about the game, because my friends and I had a lot of questions we wanted answered.  To name a few that will be addressed in this project:

- How well do we perform on different maps?
- Is there a way to determine whether or not we're improving?
- Why do we get destroyed some rounds and do great other rounds?  

It just so happens that Halo 5 has a very robust API with far more information than I was able to tackle with this project.  Nevertheless, I knew that I would finally be able to answer some questions that my friends and I have had for months.

# Business Problem

343 Industries is on the verge of releasing Halo Infinite, likely the most anticipated game of the decade so far.  The stakes are very high, not just for 343, but also for the millenials that grew up with the game.

It has been said that Halo Infinite will be a "10 year game," with regular updates and maintenance.  How can 343 keep players engaged for that length of time?  Creating a fun experience for players is obviously first and foremost, but based on the information I now know 343 tracks in Halo 5, I would argue that there is room for improved engagement through graphical analysis.  

Further, I believe that by providing more information to the player could position Halo Infinite to break into the 'core' (i.e. hyper competitive) gaming space.  The ability to tell a player they're improving, how well they do on certain maps - more information like this reveals the complexity of the game, and with improved knowledge could bring more engagment and more desire to not only play against others, but play against yourself by improving your own performance figures.

## Data

This data was sourced using the Halo Public API (Beta).  The API is a rich source of data containing information not only about individual players but also about extensive match results.  By combining multiple API calls, we were able to source data to create interesting visuals depicting a player's performance improvement throughout their history and to build machine learning models predicting the outcome of a match using only historical player information.

## Visualizations Depicting Player Performance

### Wins, Losses, and Ties by Month

With this graph, players can see their wins, losses, and ties for every month they have played.  This communicates a baseline performance improvement over time, and it's also interesting to see how much they have played each month.

![win_counts](./images/win_lose_tie_by_month.png)

If you look at May and June, it's evident that the first couple of months were a bit of a challenge, as the player lost more games than they won.  Over time, the rate of wins to losses varies somewhat, and the player will be able to think back on what changes they made throughout the course of time that led to improved win rates.

### K/D Over Time

K/D is a very standard performance metric in first person shooter games. Simply put, it's the number of players you eliminate in a match divided by the number of times you are eliminated. K/D comes from "Kills / Deaths."

![kill_spread](./images/kd_over_time_trailing_12.png)

This graph shows the trend for total kills in blue and the trend for total deaths in orange.  It's interesting to see that around March of 2021, the lines converge, representing a new trend of a K/D ratio greater than 1, which is a strong sign of improvement.

Depicting the convergence of these trends communicates to a player that the time they spent in game has led to a quantifiable skill increase.  Even if a player never crosses the threshold of a K/D ratio greater than 1, a visual representation of improvement is encouraging and could lead to better retention over time.

![dragon](./images/kd_2021.png)

This graph uses the same data as the previous, but it shows rolling 30 day average as opposed to rolling 365 day average for year to date.  In the case of this player, changes to their controller inputs led to improved accuracy around February 2021.  

You'll notice an increase in the K/D ratio from February through April, which the player attributed to using a controller with paddles for easier input accessibility.  In May of 2021, that controller stopped working, and the player had to revert to a standard controller.  Despite the adjustment evident throughout May, the player eventually returned to the stronger K/D ratio.

### Long Range Accuracy Over Time

![multicollinearity](./images/long_range_accuracy_over_time.png)

In this example, the player's long range accuracy is plotted using the 365 day rolling average.  The increase beginning in January of 2021 marks the time when the player understood the importance of long range combat, but the accuracy plateaued from March through April.  In May of 2021, a change in the player's aiming sensitivity setting allowed them to break through the plateau and continue improving in this metric.



# Predicting Victory Using Machine Learning and Historical Player Metrics

The second goal of this project was to determine how accurately victory could be predicted using only historical player data and match victory data.

Multiple API calls were used to compile each line of data.  Here's a quick breakdown for how this was accomplished:

- Using a list of 850 unique Xbox Live gamertags, 25 Match ID's and dates were pulled for each gamertag using the Player Match History API call
- For each of the players 25 Match ID's, full match results were pulled from Match Result - Arena API call
- Each match result was compiled into a single dataframe which included game mode, playlist, map, and whether the player won, lost, and a list of gamertag's on the player's team and on their opponent's team
- From the single match dataframe, each player's historical performance by game mode was pulled using the Player Service Records - Arena API call
- Each match was then compiled into a final dataframe before another function converted match results and historical player statistics into a single line of data, which was required for the machine learning models
- Of the 17,143 matches compiled for the dataframe, 5,306 were used for the model after filtering for the 'Capture the Flag' game mode and the 'Super Fiesta Party' playlist

## Models, Scalers, and Datasets

Many models, scalers, and variations of the modeling dataset were tested to find the optimal model for predicting victory using player statistics.  

**Models**:

- Logistic Regression
- Random Forests
- Support Vector Machines
- XGBoost

**Scalers**:

- Standard Scaler
- Robust Scaler
- Power Transformer

**Datasets**:

- <u>All player performance metrics broken out by individual players</u> (e.g. all metrics for each player represented individually)
- <u>Total lifetime performance metrics</u> (e.g. total weapon damage, total shots landed, total melee damage for players 1, 2, 3, and 4 and opponents 1, 2, 3, and 4)
- <u>Averaged performance metrics per game</u> (e.g. weapon damage per game, shots landed per game, melee damage per game players 1, 2, 3, and 4 and opponents 1, 2, 3, and 4))
- <u>Total and averaged performance metrics condensed by team average</u> (e.g. player team total weapon damage, enemy team total weapon damage, etc)

# Best Model: Logistic Regression, Power Transformer, Averaged Per Game Performance Metrics by Team


After testing all the models, the best performance came from logistic regression using the power transformer and the averaged per game performance metrics by team.

#### Performance

    Cross validation mean: 	72.29%
    Training Accuracy: 		73.07%
    Test Accuracy: 			72.73%

              precision    recall  f1-score   support

           0       0.69      0.65      0.67       673
           1       0.75      0.79      0.77       926

    accuracy                           0.73      1599
    macro avg       0.72     0.72      0.72      1599
    weighted avg    0.73     0.73      0.73      1599

![logistic](./images/best_model.png)

### Interpretation

The model is more precise at predicting victory over defeat, and this might be due to the fact that the matches compiled for the dataframe came from players that were fairly experienced in the Super Fiesta Party playlist.  In the future, it might be worth exploring matches from competitors with less play time and less experience in the playlist.

## Model Coefficients and Feature Importances

Using our best model, let's take a look at the logistic regression coefficients to interpret feature importance.  The first 10 features on the bar graph below represent the features the model used to predict victory, and the bottom 10 represent the features used to predict defeat.

![logistic](./images/feature_importances.png)

The player team's average win rate between the 4 teammates is the strongest predictor of victory.  Interestingly, player team's average shots landed per game is not a feature that was anticipated to have high predictive quality since it's only one piece of the accuracy feature, which measure shots landed per game divided by shots fired per game.  Total games won, total games completed, and total time played were also highly influential, and the importance of those features reflect the initial hypotheses before modeling was conducted.




# Conclusions and Recommendations

### Visualizations
Visuals depicting historical performance and player growth aren't found in many major titles. After constructing some myself with my own data, I firmly believe that visuals like these are low hanging fruit for developers hoping to increase engagement and player retention.

Exploring K/D improvement over time reaffirms many of the decisions I made while trying to become a better team player. There is a growing community of creaters on YouTube who specialize in skills, tactics, and controller setting optimization. The popularity of these channels is surely evidence that gamers do indeed care about becoming better players.

For example, providing a K/D ratio over time similar to the one I created here but with visual markers indicating controller setting changes, weapon loadout changes, or anything defined by the player could alleviate frustration caused by a sense of failure and defeat when first starting a game.

Playing devil's advocate, I will admit that providing increased transparency in performance could fuel the ire of this generation's anger with developers and might have the opposite effect.

I recmmend developers experiment with offering these tools to players. Properly framed, these visuals could increase satisfaction in more seasoned players and offer guidance to newer players.

### Modeling
For this specific playlist and with players who were most likely more skilled than average, we were able to predict the victor of a match with 72.73% accuracy using only information gathered by the API and no details about what actually occurred during the match.  

While I admittedly have no knowledge on best practices in ensuring a positive player experience, I believe an ideal matchmaking algorithm should not be predictable above a certain threshold, ideally not much higher than 50%.

It is entirely possible that matchmaking algorithms are already optimized to meet this ideal standard.  Perhaps sourcing modeling data from more skilled players in a very specific playlist would naturally lead to a higher than desired predictive quality simply because there are not enough equally skilled players entering matchmaking to ensure an even match at various hours of the day.

However, if that's not the case, a solution to uneven matchmaking might come in the form of a machine learning model as simple and efficient as logistic regression using readily available player data.  If something like this isn't being used, it could be implemented experimentally.

I should note that none of the modeling was conducted with ranked matchmaking, which certainly exists in Halo 5 and many other competitive games.  That system is likely more nuanced and robust, and deserves its own round of modeling and analysis.


# Next Steps

### Visuals
Conducting market research or simply raising the topic on social media or a game's subreddit would offer immediate insight into what players might like to know about their performance.  It would be important to develop an understanding of which visuals are fun and engaging and which visuals could potentially cause more frustration.  

Additionally, on top of personal improvement metrics, there is an abundance of post-match data in Halo 5 that is currently going under-utilized.  Here are a few ideas that could be explored for enhancing the match report:
- 2D / 3D heat maps depicting areas of high activity during the match
- A one dimendsional bar depicting who was in the lead throughout the duration of the match
- Sueprlative awards granted to each player (best long distance, most destruction, best accuracy, e tc.)

### Modeling 
Regarding the Super Fiesta Party playlist, where players spawn with random weapons throughout the match, there exists a 'Match Events' API call that details nearly every action that happened in any given match.  Most importantly, this provides information on what weapons players spawned with throughout the match.  Given the fact that the weapons are randomized, frequenters of Super Fiesta Party will (or should) freely admit that luck with the random weapons varies substantially.

This project was originally concieved with this in mind, and the goal was to predict victory based on random weapon spawns alone.  The hurdle we encountered was that there was not a way to decode the +100 weapon variants.  343 Industries admitted in a forum post that adding this to the API would not be trivial, and given the API is technically a beta, they're under no obligation to give us this information.  However, it should be possible to decode the weapon variants through some individual data collection conducted through custom matches.

Finally, we would like to exapnd our modeling dataset to a variety of skill levels and playlists, which will be possible by identifying players that meet this criteria.  It would certainly be worthwhile to determine whether or not ranked matchmaking has the same level of predictive quality.

## For More Information

See the full analysis in the [Jupyter Notebook](./Johnny Dryman - Phase 3 Project Notebook.ipynb) or review this [presentation](./Johnny Dryman - Phase 3 Project Presentation.pdf).

For additional info, contact Johnny Dryman at [johnnydryman@gmail.com](mailto:johnnydryman@gmail.com)

## Repository Structure

```
├── data
├── images
├── README.md
├── Johnny Dryman - Phase 3 Project Presentation.pdf
└── Johnny Dryman - Phase 3 Project Notebook.ipynb
```