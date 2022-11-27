import Stack from '@mui/material/Stack';
import SettingsIcon from '@mui/icons-material/Settings';
import Typography from '@mui/material/Typography';
import AppBar from '@mui/material/AppBar';
import IconButton from '@mui/material/IconButton'
import Menu from '@mui/material/Menu';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import Toolbar from '@mui/material/Toolbar'
import PowerSettingsNewIcon from '@mui/icons-material/PowerSettingsNew';
import FlaskService from '../Services/FlaskService'
import {PixyMode} from '../Model/PixyMode'
import {BrightnessSlider} from './BrightnessSlider'
import {ColorPicker} from './ColorPicker'
import { useState } from 'react';

export function MainAppBar(props) {
    const [anchorEl, setAnchorEl] = useState(null);

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleMenu = (event: MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };

    return (
        <AppBar position="static">
            <Toolbar variant="dense">
                <IconButton
                color="inherit"
                sx={{ mr: 2 }}
                onClick={() => {
                    FlaskService.setMode(PixyMode.OFF)
                    .then((_) => {
                        props.setCurrentMode(PixyMode.OFF)
                    })
                    .catch((err) => {
                      console.log(err)
                    });
                }} 
                >
                    <PowerSettingsNewIcon />
                </IconButton>
                <Tabs 
                    value={props.tabIndex} 
                    onChange={props.setTabIndex} 
                    indicatorColor="secondary" 
                    textColor="inherit"
                >
                    <Tab label="Clock"/>
                    <Tab label="Spotify"/>
                </Tabs>
                <Typography 
                    align="right"
                    mr
                    sx={{ flexGrow: 1, mr: 2 }}
                    > 
                    Currently: {props.currentMode} 
                </Typography>
                <div>
                    <IconButton
                        size="large"
                        color="inherit"
                        onClick={handleMenu}
                    >
                        <SettingsIcon />
                    </IconButton>
                    <Menu
                        anchorEl={anchorEl}
                        anchorOrigin={{
                        vertical: 'top',
                        horizontal: 'right',
                        }}
                        keepMounted
                        transformOrigin={{
                        vertical: 'top',
                        horizontal: 'right',
                        }}
                        open={Boolean(anchorEl)}
                        onClose={handleClose}
                    >
                        <Stack spacing={2} sx={{ padding: 2, width: 200 }}>
                            <BrightnessSlider />
                            <ColorPicker />
                        </Stack>
                    </Menu>
                </div>
                
            </Toolbar>
        </AppBar>
        );
}