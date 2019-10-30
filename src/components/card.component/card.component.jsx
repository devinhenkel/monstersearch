import React from 'react';
import './card.style.css';

export const Card = (props) => {
    return(
        <div key={props.monster.id} className="monster-card-container">
            <img className="monster-image" alt="monster" src={`https://robohash.org/${props.monster.id}?set=set3`} />
            <div className="monster-name">{props.monster.name}</div>
            <div className="monster-email">{props.monster.email}</div>
        </div>
    );
}