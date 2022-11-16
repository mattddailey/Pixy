import Button from '@mui/material/Button';
import {PixyMode} from '../Model/PixyMode'
import FlaskService from '../Services/FlaskService'
import { useEffect, useState } from 'react';

export function SpotifyTab(props) {

    const [isButtonDisabled, setIsButtonDisabled] = useState(false);

    useEffect(() => {
        const spotifyOn = props.currentMode === PixyMode.SPOTIFY
        setIsButtonDisabled(spotifyOn)
      }, [props.currentMode]);

    return (
        <Button 
            disabled={isButtonDisabled}
            onClick={() => {
                FlaskService.setMode(PixyMode.SPOTIFY)
                .then((_) => {
                  props.setCurrentMode(PixyMode.SPOTIFY)
                })
                .catch((err) => {
                  console.log(err)
                });
            }} 
            variant="contained" 
            color="success" 
            fullWidth={true}
        >
            Enable
        </Button>
    );
}