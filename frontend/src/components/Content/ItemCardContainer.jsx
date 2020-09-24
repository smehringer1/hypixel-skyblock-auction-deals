import React from 'react'
import ItemCard from './ItemCard'
import  {Paper, Grid} from '@material-ui/core/'

export default function ItemCardContainer(props) {
    const sortCompare = (a, b) => {
        switch (props.sort) {
            case 0: 
                return a.item_name.localeCompare(b.item_name)
            case 1:
                return a.lowest_price - b.lowest_price
            case 2:
                return b.lowest_price - a.lowest_price
            case 3:
                return b.percentage - a.percentage
            case 4:
                return a.percentage - b.percentage
        }
    }

    var data = props.data;
    data.sort(sortCompare)
    if (props.search !== ""){
        var queriedData = []
        data.forEach(item => {
            if (item.item_name.includes(props.search)) {
                queriedData.push(item)
            }
        })
        data = queriedData
    }

    const items = data.map((item) =>
        <Grid item xs={12} sm={6} md={4} lg={2} key={item.item_name}>
            <Paper style={{padding: 15}}>
                <ItemCard key={item.item_name} item={item}/>
            </Paper>
        </Grid> 
    )

    
    return (
        <Grid container spacing={2} style={{ margin: 10 }}>
            {items}
        </Grid>
    ) 
    
    
}
