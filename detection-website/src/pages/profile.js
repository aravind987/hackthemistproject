import React from 'react'

import './profile.css'

function FillBar({percentage, color, name}) {
    return (<div className="stats">
        <div className="fill-bar">
            <div className="progress-bar" style={{"--percentage": percentage*100 + '%', "--color": color}}/>
        </div>
        <p>{name}</p>
    </div>)
}

function Profile({image, username, percentRacist, percentHate, percentNeutral}) {
    return (
        <div className="profile-container">

            <div className="profile-top">
                <img src={image}/>
                <p>{'@' + username}</p>
            </div>

            <div className="profile-right">
                <div className="recommendation">
                    <h1>Recommendations</h1>
                    <p>...</p>
                </div>
                <div className="actions">
                    <h1>Actions</h1>
                    <button>Report</button>
                    <button>Ban</button>
                </div>
            </div>

            <div className="profile-stats">
                <h1>Statistics</h1>
                <FillBar percentage={percentRacist} name = {"Racist " + Math.floor(percentRacist * 100) + "%"} color="#3C7A89"/>
                <FillBar percentage={percentHate} name = {"Hate " + Math.floor(percentHate * 100) + "%"} color="#F79F79"/>
                <FillBar percentage={percentNeutral} name = {"Neutral " + Math.floor(percentNeutral * 100) + "%"} color="#D3F3EE"/>
            </div>

        </div>
    )
}

export default Profile