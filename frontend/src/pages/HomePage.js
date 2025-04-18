import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  makeStyles,
} from '@material-ui/core';
import VerifiedUserIcon from '@material-ui/icons/VerifiedUser';
import SecurityIcon from '@material-ui/icons/Security';
import BlockIcon from '@material-ui/icons/CallToAction';

const useStyles = makeStyles((theme) => ({
  heroContent: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(8, 0, 6),
  },
  heroButtons: {
    marginTop: theme.spacing(4),
  },
  cardGrid: {
    paddingTop: theme.spacing(8),
    paddingBottom: theme.spacing(8),
  },
  card: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    transition: 'transform 0.2s',
    '&:hover': {
      transform: 'scale(1.03)',
    },
  },
  cardContent: {
    flexGrow: 1,
  },
  cardIcon: {
    fontSize: 50,
    margin: theme.spacing(2, 0),
    color: theme.palette.primary.main,
  },
}));

function HomePage() {
  const classes = useStyles();

  return (
    <div>
      <div className={classes.heroContent}>
        <Container maxWidth="sm">
          <Typography component="h1" variant="h2" align="center" color="textPrimary" gutterBottom>
            Secure Identity Verification
          </Typography>
          <Typography variant="h5" align="center" color="textSecondary" paragraph>
            A blockchain-based AI solution for privacy-preserving identity verification.
            Protect your personal data while confidently proving your identity.
          </Typography>
          <div className={classes.heroButtons}>
            <Grid container spacing={2} justifyContent="center">
              <Grid item>
                <Button variant="contained" color="primary" component={RouterLink} to="/verify">
                  Verify Your Identity
                </Button>
              </Grid>
              <Grid item>
                <Button variant="outlined" color="primary" component={RouterLink} to="/profile">
                  Manage Your Profile
                </Button>
              </Grid>
            </Grid>
          </div>
        </Container>
      </div>
      
      <Container className={classes.cardGrid} maxWidth="md">
        <Grid container spacing={4}>
          <Grid item xs={12} sm={4}>
            <Card className={classes.card}>
              <CardContent className={classes.cardContent}>
                <VerifiedUserIcon className={classes.cardIcon} />
                <Typography gutterBottom variant="h5" component="h2">
                  Secure Verification
                </Typography>
                <Typography>
                  Verify your identity using advanced biometric technology and government ID validation,
                  with AI-powered fraud detection for maximum security.
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" color="primary" component={RouterLink} to="/verify">
                  Get Started
                </Button>
              </CardActions>
            </Card>
          </Grid>

          <Grid item xs={12} sm={4}>
            <Card className={classes.card}>
              <CardContent className={classes.cardContent}>
                <BlockIcon className={classes.cardIcon} />
                <Typography gutterBottom variant="h5" component="h2">
                  Blockchain Technology
                </Typography>
                <Typography>
                  Your identity data is securely stored on a decentralized blockchain,
                  ensuring immutability and giving you complete control over access.
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" color="primary" component={RouterLink} to="/permissions">
                  Manage Access
                </Button>
              </CardActions>
            </Card>
          </Grid>

          <Grid item xs={12} sm={4}>
            <Card className={classes.card}>
              <CardContent className={classes.cardContent}>
                <SecurityIcon className={classes.cardIcon} />
                <Typography gutterBottom variant="h5" component="h2">
                  Privacy Protection
                </Typography>
                <Typography>
                  Advanced zero-knowledge proofs and homomorphic encryption ensure
                  your personal data remains private while still enabling verification.
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" color="primary">
                  Learn More
                </Button>
              </CardActions>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </div>
  );
}

export default HomePage; 