import './App.css';
import {MainAppBar} from './Components/AppBar'
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import { useState } from 'react';

function App() {

  // current mode state
  
  // login state

  // tab state
  const [tabIndex, setTabIndex] = useState(0);
  const handleTabChange = (_, newTabIndex) => {
    setTabIndex(newTabIndex);
  };

  return (
    <Box>
      <MainAppBar setTabIndex={handleTabChange} tabIndex={tabIndex} ></MainAppBar>
      <Box sx={{ padding: 2 }}>
        {tabIndex === 0 && (
            <Button variant="contained" color="success" fullWidth={true}>Enable</Button>
        )}
      </Box>
    </Box>
  );
}

function spotify() {
  alert('Starting spotify');
  fetch('http://localhost:5000/spotify', { method: 'GET' })
    .then((response) => {
      if(!response.ok) throw new Error(response.status);
      else console.log("Spotify call success")
    })
}

function revoke() {
  alert('Turning off');
  fetch('http://localhost:5000/revoke', { method: 'GET' })
    .then((response) => {
      if(!response.ok) throw new Error(response.status);
      else console.log("revoke success")
    })
}

export default App;
