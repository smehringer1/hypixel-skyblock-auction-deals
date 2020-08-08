import React, {useState, useEffect } from 'react'
import ItemCard from '../ItemCard/ItemCard'
import './ItemCardContainer.scss'

export default function ItemCardContainer() {
    const [ data , setData ] = useState([]);
    
    useEffect(() => {
        fetch('/api/auctions/deals')
        .then(res => res.json())
        .then(data => {
            setData(data)
        })
    }, []) 

    const items = data.map((item) => 
        <div key={item.item_name}>
            <ItemCard key={item.item_name} item={item}/>
        </div>
    )

    return (
        <div className='item-container'>
            {items}
        </div>
    )
}
