
# TwitchRecover with Cloudflare bypass

First of all, I would like to express my gratitude to the original author of https://github.com/tanersb/TwitchRecover for their amazing work. This project is built upon their optimization.

Usage: 

1. As a first step, Download the zip file and unzip it, open command prompt at project directory root and run ```pip install -r requirements.txt ```to install required packages

2. Sign up at https://scrapingant.com/ and go to https://app.scrapingant.com/dashboard to copy your API key.

3. Open recover.py in the code editor, locate the variable api_key and replace the value with your API key 
   (e.g., api_key = "YOUR_API_KEY"), then save the file.

4. Using a Twitch Tracker or Streams Charts link: 

        You can use the Twitch Tracker or Streams Charts link of a stream to directly get the VOD links. 


        i.e. https://twitchtracker.com/blastpremier/streams/46313458365


        i.e. https://streamscharts.com/channels/blastpremier/streams/46313458365

5. Run recover.py and copy the link from Twitch Tracker or Streams Charts as input.



## How do I use this link


(recommend) Copy the link to N_m3u8DL-CLI-SimpleG(https://github.com/nilaoda/N_m3u8DL-CLI) to initiate the download.

or

Use the VLC media player. 
CTRL + N (open network stream) and paste this link.



