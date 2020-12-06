# Spotify song info website

Gets song info using spotify url or by finding the `Now playing Song` of the user. Made using python

## Testing out the site
The site can be found [here](https://spot-info.herokuapp.com). Hosted by [Heroku](https://www.heroku.com) for free

Must log-in to spotify. 

## Running it yourself
1. Clone the repository (`git clone https://github.com/kevin-samson/Spotify-song-info-website.git`) or download the code
2. Install reqierd liberies (`pip install -r requierments.txt`) 
3. Edit `CLI_ID`, `CLI_SEC` and `REDIRECT_URI` in [`/spoti/main.py`](https://github.com/kevin-samson/Spotify-song-info-website/blob/main/spoti/main.py). 

   `CLI_ID` and `CLI_SEC` can be found on [Spotify Devlopers Dashboad](https://developer.spotify.com/dashboard/). 
   Create a new app and make sure that `REDIRECT_URI` is the same as your domain name 
   
   
   Note:- If your running thee web server your on computer, `REDIRECT_URI` is `http://127.0.0.1:5000/api_callback` 

4. Run the program (`python run.py`)

