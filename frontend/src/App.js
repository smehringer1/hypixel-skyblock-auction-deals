import React, {useState, useEffect} from 'react';
import Navbar from './components/Navbar/Navbar'
import Sidebar from './components/Sidebar/Sidebar'
import ItemCardContainer from './components/Content/ItemCardContainer'
import './App.css'

function App() {
  var defaultSettings = { searchQuery: "", percentThreshold: 0.15, minPrice: 0 }
  const [settings, setSettings] = useState(defaultSettings);
  const [ data , setData ] = useState([]);
  const [refresh, setRefresh] = useState(false);

  const submitHandler = (searchString, minPrice, percentThreshold, sort) => {
    setSettings({
      searchQuery: searchString,
      percentThreshold: percentThreshold / 100,
      minPrice: minPrice,
      sort: sort
    });
  }

  const refreshHandler = () => {
    setRefresh(!refresh)
  }

  useEffect(() => {
    fetch(`/api/auctions/deals?percent=${settings["percentThreshold"]}&minprice=${settings["minPrice"]}`)
        .then(res => res.json())
        .then(data => {
            setData(data)
        })
  }, [settings['minPrice'], settings['percentThreshold'], settings['searchQuery'], refresh]) 

  return (
    <div>
      <Navbar onRefresh={refreshHandler}/>
      <div style={{display: 'flex', flexDirection: 'row'}}>
        <Sidebar onFormSubmit={submitHandler}/>
        <ItemCardContainer sort={settings['sort']} search={settings['searchQuery']} data={data}/>
      </div>
    </div>
  );
}

export default App;
