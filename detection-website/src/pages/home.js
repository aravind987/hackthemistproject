import React from 'react'

import './home.css';

import { TwitterTweetEmbed } from 'react-twitter-embed'
import { useState, useEffect } from 'react'

import Profile from './profile.js'

var currentText;


function TweetEmbed({tweet}) {
    return <div className="tweet-embed">
            <div className="tweet-profile">
                <img className="tweet-image" src={tweet.image}/>
                <p className="tweet-user">{'@' + tweet.username}</p>
            </div>
            <p className="tweet-text">{tweet.text}</p>
            <p className="tweet-date">{tweet.time}</p>
    </div>

}


function Home() {


    const [ currentTwitter, setCurrentTwitter] = useState(null)

    function retrieveClasses(keywords: string) {

        if(keywords == null)
            keywords = ''

        console.log("Sending " + keywords + " From React")
        fetch('/getClass', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                keywords: keywords.split(",")
            })
        }).then(res => res.json())
        .then((data) => {
            setCurrentTwitter(data)
        })
    }

    useEffect(() => retrieveClasses(currentText), [])

    return (
        <div className="parent-container">
            <div>
                <div className="text-input">
                    <form className="text-form">
                        <label>Key Words</label>
                        <input type="keyword" placeholder="Enter Something"
                        onChange = {(event) => {currentText = event.target.value}}></input>
                    </form>

                    <button className="submit-button" onClick={() => retrieveClasses(currentText)}>Test</button>

                </div>

                <div className="twitter-container">
                    {currentTwitter != null && currentTwitter.map((tweet) => {
                    return <TweetEmbed tweet={tweet}/>})}
                </div>
            </div>
            <Profile/>
        </div>
    );

}

export default Home;