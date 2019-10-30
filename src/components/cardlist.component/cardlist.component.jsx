import React from 'react';
import {Card} from '../card.component/card.component'
import './cardlist.style.css';

export const CardList = (props) => {
    return (
    <div className="card-list">
        {
            props.monsters.map(monster => 
            
                <Card key={`card ${monster.id}`} monster={monster} />
            
            )
        }
    </div>
    )
}

