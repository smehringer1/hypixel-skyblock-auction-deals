import React from 'react'
import IconButton from '@material-ui/core/IconButton'
import RefreshIcon from '@material-ui/icons/Refresh'
import './Navbar.scss'

export default function Navbar(props) {
    return (
        <nav className="navbar">
            <div className="contents">
                <h1 className="title">Auction Deals</h1>
                <IconButton onClick={props.onRefresh} style={{marginLeft : 10}}>
                    <RefreshIcon/>
                </IconButton>
            </div>
        </nav>
    )
}
