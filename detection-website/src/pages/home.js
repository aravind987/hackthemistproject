import React from 'react'

import './home.css';

import { TwitterTweetEmbed } from 'react-twitter-embed'
import { useState, useEffect } from 'react'

import Profile from './profile.js'

var currentText;

var defaultProfile = {
    image: "https://scontent-yyz1-1.xx.fbcdn.net/v/t39.30808-6/308487577_523808733083795_2015773722187850021_n.png?_nc_cat=107&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=uXF-ArkDCnAAX9_bgtN&_nc_ht=scontent-yyz1-1.xx&oh=00_AfCJAxcfz92uwXUBP6GtYx4FDuIqWT6pEdgG6p8ryq5m_Q&oe=641C4E94",
    username: "Example",
    percentRacist: 0.0,
    percentHate: 0.0,
    percentNeutral: 0.0
}

function Home() {

    const [ currentTwitter, setCurrentTwitter] = useState(null)
    const [ profileDisplay, setProfileDisplay] = useState(defaultProfile)


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

    const [ freezeTop, setFreezeTop ] = useState('relative');
    const [ padTwitter, setPadTwitter ] = useState('unpadded');

    const stickNavbar = () => {
        if (window !== undefined) {
            let windowHeight = window.scrollY;
            if(windowHeight > 180) {
                setFreezeTop('fixed');
                setPadTwitter('padded');
            } else {
                setFreezeTop('relative');
                setPadTwitter('unpadded');
            }
        }
    };

    window.addEventListener('scroll', stickNavbar);



    return (
        <div className="parent-container">
            <div className="comment-container">
                <div className={"text-input " + freezeTop}>
                    <form className="text-form">
                        <label>Key Words</label>
                        <input type="keyword" placeholder="Enter Something"
                        onChange = {(event) => {currentText = event.target.value}}></input>
                    </form>

                    <button className="submit-button" onClick={() => retrieveClasses(currentText)}>Test</button>

                </div>

                <div className={"twitter-container " + padTwitter}>
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