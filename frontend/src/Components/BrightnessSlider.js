import Slider from '@mui/material/Slider';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { useEffect, useState } from 'react';
import FlaskService from '../Services/FlaskService'

export function BrightnessSlider(props) {
    const [brightness, setBrightness] = useState(30);

    const handleChange = (event: Event, newValue: number | number[]) => {
        setBrightness(newValue);
    };

    const handleMouseUp = () => {
        FlaskService.setBrightness(brightness)
    };

    useEffect(() => {
    FlaskService.getBrightness()
    .then((brightness) => {
        setBrightness(Number(brightness))
    });
    }, []);

    return (
        <Stack spacing={2}>
            <Typography>
            Brightness: {brightness}%
            </Typography>
            <Slider value={brightness} onChange={handleChange} onMouseUp={handleMouseUp} onTouchEnd={handleMouseUp}></Slider>
        </Stack>
    )
}