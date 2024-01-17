# youtube-links-to-playlist
Create a Youtube playlist from a list of youtube video links

## Setting up API access

This script requires you to set up API access yourself. First go [to the Youtube Data API overview ](https://developers.google.com/youtube/v3/getting-started) and follow the instructions there to create a project with access to the Youtube Data API enabled.

Then, add yourself as a test user in APIs & Services -> OAuth Consent Screen -> Add users.

Finally, download a client secrets file in APIs & Services -> Credentials and creating an OAuth 2.0 client id. Download the resulting JSON file and save it as `client_secret.json` in the same directory as this script.

## Using the script

Once you've set up API access and created the `client_secret.json` file, you can run the script as follows 
```
echo -e "https://www.youtube.com/watch?v=dQw4w9WgXcQ\nhttps://www.youtube.com/watch?v=xvFZjo5PgG0" | python main.py TITLE
```

For more information on available options (such as editing the description or privacy status of the playlist), run
```
python main.py --help
```
