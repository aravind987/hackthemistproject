import './App.css';

import { TwitterTweetEmbed } from 'react-twitter-embed'
import { useState, useEffect } from 'react'

var currentText;

async function retrieveClasses(text) {

}

function App() {

    const [ currentTwitter, setCurrentTwitter] = useState(null)

    function retrieveClasses(text) {
        console.log("Sending " + text + " From React")
        fetch('/getClass', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                text: text
            })
        }).then(res => res.json())
        .then((data) => {
            setCurrentTwitter(data[0])
        })
        console.log(currentTwitter)
    }

    useEffect(() => retrieveClasses(currentText), [])

    return (
        <div className="parent-container">
            <div className="text-input">
                <form className="text-form">
                    <label>Key Words</label>
                    <input type="keyword" id="fname" name="fname" placeholder="Enter Something"
                    onChange = {(event) => {currentText = event.target.value}}></input>
                </form>

                <button className="submit-button" onClick={() => retrieveClasses(currentText)}>Test</button>

            </div>

            <div className="twitter-container">
                {currentTwitter}
            </div>
        </div>
    );
}

export default App;