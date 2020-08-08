import React from 'react'
import './ItemCard.scss'

export default function ItemCard({ item }) {
    
    return (
        <div className="itemCard">
            <h3>{item.item_name}</h3>
            <p>Lowest price: {item.lowest_price.toLocaleString()}</p>
            <p>Second lowest price: {item.second_lowest_price.toLocaleString()}</p>
            <p>{Math.round((1 - item.percentage) * 100)}% off</p>       
        </div>
    )
}
