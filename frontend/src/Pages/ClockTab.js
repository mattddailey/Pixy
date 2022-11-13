import Button from '@mui/material/Button';
import {PixyMode} from '../Model/PixyMode'
import FlaskService from '../Services/FlaskService'
import { useEffect, useState } from 'react';

export function ClockTab(props) {

    const [isButtonDisabled, setIsButtonDisabled] = useState(false);

    useEffect(() => {
        const clockOn = props.currentMode === PixyMode.CLOCK
        setIsButtonDisabled(clockOn)
      }, [props.currentMode]);

    return (
        <Button 
            disabled={isButtonDisabled}
            onClick={() => {
                FlaskService.startClock()
                .then((_) => {
                  props.setCurrentMode(PixyMode.CLOCK)
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