import React, { useState } from 'react';
import '../App.css';


function PlaylistButton(props) {
    const [playlistString, setPlaylistString] = useState('');

    const handleButtonClick = () => {
        fetch('/createPlaylist').then(response => response.text())
        .then(data => setPlaylistString(data))
        .catch(error => console.error('Error:', error))
    };

    return (
        <div className="playlistCreator">
            <button className="spotify-button" onClick={handleButtonClick}>Create Playlist</button>
            <h3 className="playlist-confirmation">{playlistString}</h3>
        </div>
    );
};

export default PlaylistButton;