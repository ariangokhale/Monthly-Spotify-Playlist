# Monthly Playlist Creator

### This application allows a user to log in to their Spotify account to see their top 15 most played songs from the past month and then create a playlist from it. Songs are listed in order from most played to least along with the artist name, album title, album cover, and like to an audio preview of the song (click song title).

## Technology Used

### The server side is a Flask API that accesses the user's listening history through the Spotify API. It makes use of the Spotipy library and OAuth to handle user log-in/caching as well as Spotipy's built in methods to create playlists. The Flask API then sends data to React to display it to the user as needed. 