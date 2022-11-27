import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { RgbaColorPicker } from "react-colorful";
import { useState } from 'react';

export function ColorPicker() {
    const [color, setColor] = useState({ r: 200, g: 150, b: 35, a: 0.5 });

    return (
        <Stack spacing={2}>
            <Typography>
            Primary Color:
            </Typography>
            <RgbaColorPicker color={color} onChange={setColor} />
        </Stack>
    )
}