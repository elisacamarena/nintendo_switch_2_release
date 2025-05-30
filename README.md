# Final project - Applied Econometrics II
## :video_game: Nintendo Switch 2 release
\
This repository is the final project for my Applied Econometrics II class.
The main purpose of the project is to build a well-documented data scraping pipeline to extract comments from YouTube using the Youtube Data API. 
\
\
The code extracts comments from the Nintendo Switch 2 [overview trailer](https://www.youtube.com/watch?v=9flte56erE8) to build a database and then classifies them into "positive" and "negative" usign TextBlob, a natural language processing (NLP) library. Finally, it graphs the results and shows the sentiment distribution.


## What does this repo contain?
 ```
  nintendo_switch_2_release/
  ├── code/
  │   └── scrape_comments.py    
  └── data/
      └── comments.csv
      └── fig1.png
  ├── .gitignore
  ├── README.md
  ├── requirements.txt         
  ```

## How can you replicate this project?
1. Clone the repository
2. Set up a virtual environment
3. Make sure you have a YouTube Data API v3 key saved in a private .env file 
4. Run scrape_comments.py

Done! You should now have an updated pie chart showing the distribution of positive and negative comments.
