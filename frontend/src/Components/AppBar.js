import AccountCircle from '@mui/icons-material/AccountCircle';
import Typography from '@mui/material/Typography';
import AppBar from '@mui/material/AppBar';
import IconButton from '@mui/material/IconButton'
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import Toolbar from '@mui/material/Toolbar'

export function MainAppBar(props) {
    return (
        <AppBar position="static">
          <Toolbar variant="dense">
            <Tabs 
                value={props.tabIndex} 
                onChange={props.setTabIndex} 
                indicatorColor="secondary" 
                textColor="inherit"
            >
                <Tab label="Spotify"/>
            </Tabs>
            <Typography 
                align="right"
                mr
                sx={{ flexGrow: 1, mr: 2 }}
                > 
                Spotify 
            </Typography>
            <IconButton
                size="large"
                color="inherit"
            >
                <AccountCircle />
            </IconButton>
          </Toolbar>
        </AppBar>
        );
}