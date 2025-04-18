import React from 'react';
import { makeStyles, Typography, Container, Link, Grid } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  footer: {
    padding: theme.spacing(3, 2),
    marginTop: 'auto',
    backgroundColor: theme.palette.grey[200],
  },
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  links: {
    marginBottom: theme.spacing(2),
  },
  linkItem: {
    margin: theme.spacing(0, 1),
  },
}));

function Footer() {
  const classes = useStyles();
  const currentYear = new Date().getFullYear();

  return (
    <footer className={classes.footer}>
      <Container maxWidth="lg" className={classes.container}>
        <Grid container justifyContent="center" className={classes.links}>
          <Grid item className={classes.linkItem}>
            <Link href="#" color="textSecondary">Privacy Policy</Link>
          </Grid>
          <Grid item className={classes.linkItem}>
            <Link href="#" color="textSecondary">Terms of Service</Link>
          </Grid>
          <Grid item className={classes.linkItem}>
            <Link href="#" color="textSecondary">Contact</Link>
          </Grid>
        </Grid>
        <Typography variant="body2" color="textSecondary" align="center">
          {"© "}
          {currentYear}
          {" PrivacyID. All rights reserved."}
        </Typography>
        <Typography variant="body2" color="textSecondary" align="center">
          {"Blockchain-Based AI for Privacy-Preserving Identity Verification"}
        </Typography>
      </Container>
    </footer>
  );
}

export default Footer; 