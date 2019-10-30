import React, {Component} from 'react';
import './searchbox.style.css'

export const SearchBox = ({placeholder, handleChange}) => (
        <input 
            className="searchBox"
            type="search" 
            placeholder={placeholder} 
            onChange={handleChange} />
)