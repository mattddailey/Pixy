import './App.css';
import Box from '@mui/material/Box';
import { useEffect, useState } from 'react';
import {MainAppBar} from './Components/AppBar'
import {PixyMode} from './Model/PixyMode'
import {SpotifyTab} from './Pages/SpotifyTab'
import {ClockTab} from './Pages/ClockTab'
import FlaskService from './Services/FlaskService'

function App() {

  // current mode state
  const [currentMode, setCurrentMode] = useState(PixyMode.OFF);

  // tab state
  const [tabIndex, setTabIndex] = useState(0);
  const handleTabChange = (_, newTabIndex) => {
    setTabIndex(newTabIndex);
  };

  useEffect(() => {
    FlaskService.getMode()
    .then((res) => {
      console.log("Current mode: " + res.currentMode)
      setCurrentMode(res.curentMode)
    });
  }, []);

  return (
    <Box>
      <MainAppBar currentMode={currentMode} setCurrentMode={setCurrentMode} setTabIndex={handleTabChange} tabIndex={tabIndex} ></MainAppBar>
      <Box sx={{ padding: 2 }}>
        {tabIndex === 0 && (
          <ClockTab currentMode={currentMode} setCurrentMode={setCurrentMode}></ClockTab>
        )}
        {tabIndex === 1 && (
          <SpotifyTab currentMode={currentMode} setCurrentMode={setCurrentMode}></SpotifyTab>
        )}
      </Box>
    </Box>
  );
}

export default App;
