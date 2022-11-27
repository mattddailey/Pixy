import Slider from '@mui/material/Slider';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { useState } from 'react';

export function BrightnessSlider(props) {
    const [value, setValue] = useState(30);

    const handleChange = (event: Event, newValue: number | number[]) => {
        setValue(newValue);
    };
    return (
        <Stack spacing={2}>
            <Typography>
            Brightness: {value}%
            </Typography>
            <Slider value={value} onChange={handleChange}></Slider>
        </Stack>
    )
}