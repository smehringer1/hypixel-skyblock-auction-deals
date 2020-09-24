import React, {useState} from 'react'
import { Button, TextField, Select, MenuItem } from '@material-ui/core/'
import './Sidebar.scss'

export default function Sidebar(props) {

    const [search, setSearch] = useState("");
    const [lowestPrice, setLowestPrice] = useState(0);
    const [percentThreshold, setPercentThreshold] = useState(15); 
    const [sort, setSort] = useState(0)

    const handleSortSelection = (e) => {
        setSort(e.target.value)
    }

    return (
        <div className='sidebar'>
            <form>
                <TextField variant="standard" label="Search" onChange={(e)=> setSearch(e.target.value)}/>
                <TextField variant="standard" label="Min Price" onChange={(e)=> setLowestPrice(e.target.value)}/>
                <TextField variant="standard" label="Percent-Off Threshold" defaultValue={15} onChange={(e)=> setPercentThreshold(e.target.value)}/>
                <Select value={sort} onChange={handleSortSelection} style={{width: 200, marginTop: 15}}>
                    <MenuItem value={0}>Alphabetical</MenuItem>
                    <MenuItem value={1}>Price: Low to High</MenuItem>
                    <MenuItem value={2}>Price: High to Low</MenuItem>
                    <MenuItem value={3}>Discount: Low to High</MenuItem>
                    <MenuItem value={4}>Discount: High to Low</MenuItem>
                </Select>
                <Button style={{marginTop: 20}}variant="contained" onClick={(e) => props.onFormSubmit(search, lowestPrice, percentThreshold, sort)}>Filter</Button>
            </form>
        </div>
    )
}
