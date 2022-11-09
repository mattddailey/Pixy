import './App.css';
import Box from '@mui/material/Box';
import { useEffect, useState } from 'react';
import {MainAppBar} from './Components/AppBar'
import {PixyMode} from './Model/PixyMode'
import {SpotifyTab} from './Pages/SpotifyTab'
import FlaskService from './Services/FlaskService'

function App() {

  // current mode state
  // TODO: use enum?
  const [currentMode, setCurrentMode] = useState(PixyMode.OFF);

  // spotify state
  const [isSpotifyAuthorized, setIsSpotifyAuthorized] = useState(false);

  // tab state
  const [tabIndex, setTabIndex] = useState(0);
  const handleTabChange = (_, newTabIndex) => {
    setTabIndex(newTabIndex);
  };

  useEffect(() => {
    FlaskService.getIsSpotifyAuthorized()
    .then((res) => {
      setIsSpotifyAuthorized(res.isLoggedIn === 'true');
    });
    FlaskService.getCurrentMode()
    .then((res) => {
      console.log("Current mode: " + res.currentMode)
      setCurrentMode(res.currentMode)
    });
  }, []);

  return (
    <Box>
      <MainAppBar currentMode={currentMode} setCurrentMode={setCurrentMode} setTabIndex={handleTabChange} tabIndex={tabIndex} ></MainAppBar>
      <Box sx={{ padding: 2 }}>
        {tabIndex === 0 && (
          <SpotifyTab currentMode={currentMode} setCurrentMode={setCurrentMode}></SpotifyTab>
        )}
      </Box>
    </Box>
  );
}

export default App;
