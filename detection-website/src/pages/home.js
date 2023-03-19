import React from 'react'

import './home.css';

import { useState, useEffect } from 'react'

import Profile from './profile.js'

var currentText;

function Home() {

    const [ currentTwitter, setCurrentTwitter] = useState(null)
    const [ profileDisplay, setProfileDisplay] = useState({
        image: "https://media.discordapp.net/attachments/757730257150279742/1080660938249736244/image.png?width=156&height=222",
        username: "Example",
        percentRacist: 0.8,
        percentHate: 0.4,
        percentNeutral: 0.2
    })

    function postAccount(username: string) {
        if(username == null)
            username = ''

        console.log("Sending " + username + " From React For Account")
        fetch('/getAccount', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                username: username
            })
        }).then(res => res.json())
        .then((data) => {
            setProfileDisplay(data[0]);
            console.log(data[0]);
        })
    }

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

    useEffect(() => postAccount(), [])


    function TweetEmbed({tweet}) {

        return <div className="tweet-embed" onClick={() => postAccount(tweet.username)}>
                <div className="tweet-profile">
                    <img className="tweet-image" src={tweet.image}/>
                    <p className="tweet-user">{'@' + tweet.username}</p>
                </div>
                <p className="tweet-text">{tweet.text}</p>
                <p className="tweet-date">{tweet.time}</p>
        </div>

    }



    useEffect(() => retrieveClasses(currentText), [])

    return (
        <div className="parent-container">
            <div className="comment-container">
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
            <Profile image={profileDisplay.image}
                     username={profileDisplay.username}
                     percentRacist={profileDisplay.percentRacist}
                     percentHate={profileDisplay.percentHate}
                     percentNeutral={profileDisplay.percentNeutral}/>
        </div>
    );

}

export default Home;