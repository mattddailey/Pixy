import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { RgbaColorPicker } from "react-colorful";
import { useEffect, useState } from 'react';
import FlaskService from '../Services/FlaskService'

export function ColorPicker() {
    const [color, setColor] = useState({ r: 200, g: 150, b: 35, a: 0.5 });

    const handleMouseUp = () => {
        FlaskService.setPrimaryColor(color.r, color.g, color.b)
    };

    useEffect(() => {
    FlaskService.getPrimaryColor()
    .then((res) => {
        setColor({ r: res.red, g: res.green, b: res.blue, a: 0.5 })
    });
    }, []);

    return (
        <Stack spacing={2}>
            <Typography>
            Primary Color:
            </Typography>
            <RgbaColorPicker color={color} onChange={setColor} onMouseUp={handleMouseUp} touchend={handleMouseUp}/>
        </Stack>
    )
}