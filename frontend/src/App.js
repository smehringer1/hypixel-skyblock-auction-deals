import React from 'react';
import Navbar from './components/Navbar/Navbar.js'
import Sidebar from './components/Sidebar/Sidebar'
import {ItemCardContainer} from './components/Content'

import './App.scss'

function App() {
  return (
    <div>
      <Navbar/>
      <div className="main-container">
        <Sidebar/>
        <ItemCardContainer/>
      </div>
    </div>
  );
}

export default App;
