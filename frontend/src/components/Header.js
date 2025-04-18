import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  makeStyles,
  Container,
} from '@material-ui/core';
import LockIcon from '@material-ui/icons/Lock';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  logo: {
    marginRight: theme.spacing(2),
    display: 'flex',
    alignItems: 'center',
  },
  logoIcon: {
    marginRight: theme.spacing(1),
  },
  title: {
    flexGrow: 1,
  },
  navButton: {
    marginLeft: theme.spacing(2),
  },
}));

function Header() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Container>
          <Toolbar>
            <div className={classes.logo}>
              <LockIcon className={classes.logoIcon} />
              <Typography variant="h6" component={RouterLink} to="/" style={{ textDecoration: 'none', color: 'white' }}>
                PrivacyID
              </Typography>
            </div>
            <div className={classes.title} />
            <Button color="inherit" component={RouterLink} to="/" className={classes.navButton}>
              Home
            </Button>
            <Button color="inherit" component={RouterLink} to="/verify" className={classes.navButton}>
              Verify Identity
            </Button>
            <Button color="inherit" component={RouterLink} to="/profile" className={classes.navButton}>
              My Profile
            </Button>
            <Button color="inherit" component={RouterLink} to="/permissions" className={classes.navButton}>
              Data Permissions
            </Button>
          </Toolbar>
        </Container>
      </AppBar>
    </div>
  );
}

export default Header; 