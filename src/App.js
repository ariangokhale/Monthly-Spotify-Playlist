import React, { useState, useEffect } from 'react';
import './App.css';
import Song from './components/Song';
import PlaylistButton from './components/Playlist';
import Login from './components/Login'

function App() {
  
  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/getTracks").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  return (
    <div>
      <h1 className="title"> Past Month Top Songs (click to listen) </h1>
      {data.map((song) => <Song previewURL={song.audio_sample_url} coverArt={song.cover_art} songName={song.name} albumName={song.album_name} artistName={song.artist}/>)}
      <PlaylistButton />
    </div>
  );
}

export default App;
