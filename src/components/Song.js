import React from 'react';
import '../App.css';

function Song(props) {
    return (
      <div className="songComponent">
        <img src={props.coverArt} heigh="60" width="60"/>
        
        <a href={props.previewURL} target="_blank"> 
            <h3 className="songName"> {props.songName} </h3>
        </a>
        <h5 className="artistName"> {props.artistName} </h5>
        <h5 className="albumName"> | {props.albumName} </h5>
      </div>
    );
  }
  
  export default Song;