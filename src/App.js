import React, { Component } from 'react';

import {CardList} from './components/cardlist.component/cardlist.component'
import {SearchBox} from './components/searchbox.component/searchbox.component'

import logo from './lab-logo-white.svg';
import './App.css';

class App extends Component {
  constructor() {
    super();

    this.state = {
      monsters: [],
      searchField: ''
    };
  }

  componentDidMount() {
    fetch('https://jsonplaceholder.typicode.com/users')
      .then(response => response.json())
      .then(users => this.setState({monsters: users}))
  }

  handleChange = (e) => {
    this.setState({searchField: e.target.value})
  }

  render() {
    const { monsters, searchField } = this.state;
    const filteredMonsters = monsters.filter(monster => 
      monster.name.toLowerCase().includes(searchField.toLowerCase())
    )
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <SearchBox placeholder="Monster Search" handleChange={this.handleChange} />
          <CardList monsters={filteredMonsters} />
        </header>
      </div>
    );
  }
}

export default App;
