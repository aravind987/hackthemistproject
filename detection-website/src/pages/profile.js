import React from 'react'

import './profile.css'

function Profile({image, username}) {
    return (
        <div className="profile-container">

            <div className="profile-top">
                <img src={image}/>
                <p>{'@' + username}</p>
            </div>

            <div className="profile-right">
                Profile Side
            </div>

            <div className="profile-stats">
                Profile Stats
            </div>

        </div>
    )
}

export default Profile