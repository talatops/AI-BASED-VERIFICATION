import React, { useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Avatar,
  Divider,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  makeStyles,
  Switch,
  FormControlLabel,
  Box,
  Chip,
} from '@material-ui/core';
import PersonIcon from '@material-ui/icons/Person';
import EmailIcon from '@material-ui/icons/Email';
import PhoneIcon from '@material-ui/icons/Phone';
import HomeIcon from '@material-ui/icons/Home';
import PublicIcon from '@material-ui/icons/Public';
import VerifiedUserIcon from '@material-ui/icons/VerifiedUser';
import SecurityIcon from '@material-ui/icons/Security';
import EventIcon from '@material-ui/icons/Event';
import BlockIcon from '@material-ui/icons/ViewModule';

const useStyles = makeStyles((theme) => ({
  container: {
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4),
  },
  paper: {
    padding: theme.spacing(3),
    marginBottom: theme.spacing(3),
  },
  avatar: {
    width: theme.spacing(10),
    height: theme.spacing(10),
    backgroundColor: theme.palette.primary.main,
  },
  section: {
    marginTop: theme.spacing(3),
  },
  divider: {
    margin: theme.spacing(3, 0),
  },
  verificationChip: {
    margin: theme.spacing(1),
  },
  blockchainInfo: {
    padding: theme.spacing(2),
    backgroundColor: theme.palette.grey[100],
    borderRadius: theme.shape.borderRadius,
    marginTop: theme.spacing(2),
  },
  infoSection: {
    marginBottom: theme.spacing(3),
  },
  verifiedIcon: {
    color: theme.palette.success.main,
    marginLeft: theme.spacing(1),
  },
  listItem: {
    padding: theme.spacing(1, 0),
  },
  privacySettings: {
    marginTop: theme.spacing(2),
  },
}));

function ProfilePage() {
  const classes = useStyles();
  
  // Mock user data - in a real app, this would come from an API
  const [user, setUser] = useState({
    firstName: 'John',
    lastName: 'Doe',
    email: 'john.doe@example.com',
    phone: '+1 (555) 123-4567',
    address: '123 Privacy Street, Secure City',
    country: 'United States',
    dateOfBirth: '1985-06-15',
    verificationStatus: {
      id: 'verified',
      biometric: 'verified',
      address: 'pending',
    },
    blockchainAddress: '0x1a2b3c4d5e6f7g8h9i0j...',
    lastVerification: '2023-10-15T14:32:45Z',
  });

  const [privacySettings, setPrivacySettings] = useState({
    shareEmail: false,
    sharePhone: false,
    shareAddress: false,
    shareDateOfBirth: false,
  });

  const handlePrivacySetting = (event) => {
    setPrivacySettings({
      ...privacySettings,
      [event.target.name]: event.target.checked,
    });
  };

  return (
    <Container maxWidth="lg" className={classes.container}>
      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Paper className={classes.paper}>
            <Box display="flex" flexDirection="column" alignItems="center">
              <Avatar className={classes.avatar}>
                {user.firstName.charAt(0)}{user.lastName.charAt(0)}
              </Avatar>
              <Typography variant="h5" component="h2" gutterBottom style={{ marginTop: 16 }}>
                {user.firstName} {user.lastName}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Identity verified with blockchain security
              </Typography>
              
              <Box mt={2} display="flex" justifyContent="center" flexWrap="wrap">
                {user.verificationStatus.id === 'verified' && (
                  <Chip
                    icon={<VerifiedUserIcon />}
                    label="ID Verified"
                    color="primary"
                    className={classes.verificationChip}
                  />
                )}
                {user.verificationStatus.biometric === 'verified' && (
                  <Chip
                    icon={<SecurityIcon />}
                    label="Biometric Verified"
                    color="primary"
                    className={classes.verificationChip}
                  />
                )}
                {user.verificationStatus.address === 'pending' && (
                  <Chip
                    label="Address Pending"
                    color="default"
                    className={classes.verificationChip}
                  />
                )}
              </Box>
            </Box>
            
            <Divider className={classes.divider} />
            
            <Typography variant="h6" gutterBottom>
              Blockchain Information
            </Typography>
            <div className={classes.blockchainInfo}>
              <Typography variant="body2" gutterBottom>
                Your identity is secured by the following blockchain address:
              </Typography>
              <Typography variant="body2" style={{ wordBreak: 'break-all' }}>
                {user.blockchainAddress}
              </Typography>
              <Box mt={2}>
                <Typography variant="body2">
                  Last verification: {new Date(user.lastVerification).toLocaleString()}
                </Typography>
              </Box>
            </div>
            
            <Box mt={3}>
              <Button variant="outlined" color="primary" fullWidth>
                View Verification History
              </Button>
            </Box>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={8}>
          <Paper className={classes.paper}>
            <Typography variant="h5" gutterBottom>
              Personal Information
            </Typography>
            <Typography variant="body2" color="textSecondary" paragraph>
              This information is securely stored with Zero-Knowledge Proofs (ZKPs) and 
              homomorphic encryption. You control who can access this data.
            </Typography>
            
            <div className={classes.infoSection}>
              <List>
                <ListItem className={classes.listItem}>
                  <ListItemIcon>
                    <PersonIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Full Name" 
                    secondary={`${user.firstName} ${user.lastName}`}
                  />
                  <VerifiedUserIcon className={classes.verifiedIcon} />
                </ListItem>
                
                <ListItem className={classes.listItem}>
                  <ListItemIcon>
                    <EmailIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Email Address" 
                    secondary={user.email} 
                  />
                </ListItem>
                
                <ListItem className={classes.listItem}>
                  <ListItemIcon>
                    <PhoneIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Phone Number" 
                    secondary={user.phone} 
                  />
                </ListItem>
                
                <ListItem className={classes.listItem}>
                  <ListItemIcon>
                    <HomeIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Address" 
                    secondary={user.address} 
                  />
                </ListItem>
                
                <ListItem className={classes.listItem}>
                  <ListItemIcon>
                    <PublicIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Country" 
                    secondary={user.country} 
                  />
                </ListItem>
                
                <ListItem className={classes.listItem}>
                  <ListItemIcon>
                    <EventIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Date of Birth" 
                    secondary={new Date(user.dateOfBirth).toLocaleDateString()} 
                  />
                  <VerifiedUserIcon className={classes.verifiedIcon} />
                </ListItem>
              </List>
            </div>

            <Divider className={classes.divider} />
            
            <Typography variant="h6" gutterBottom>
              Privacy Settings
            </Typography>
            <Typography variant="body2" color="textSecondary" paragraph>
              Control which parts of your identity information can be shared with third parties.
              These settings apply when you authorize identity verification requests.
            </Typography>
            
            <div className={classes.privacySettings}>
              <FormControlLabel
                control={
                  <Switch
                    checked={privacySettings.shareEmail}
                    onChange={handlePrivacySetting}
                    name="shareEmail"
                    color="primary"
                  />
                }
                label="Share email address with authorized services"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={privacySettings.sharePhone}
                    onChange={handlePrivacySetting}
                    name="sharePhone"
                    color="primary"
                  />
                }
                label="Share phone number with authorized services"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={privacySettings.shareAddress}
                    onChange={handlePrivacySetting}
                    name="shareAddress"
                    color="primary"
                  />
                }
                label="Share address with authorized services"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={privacySettings.shareDateOfBirth}
                    onChange={handlePrivacySetting}
                    name="shareDateOfBirth"
                    color="primary"
                  />
                }
                label="Share date of birth with authorized services"
              />
            </div>
            
            <Box mt={3} display="flex" justifyContent="space-between">
              <Button variant="contained" color="primary">
                Save Privacy Settings
              </Button>
              <Button variant="outlined" color="secondary">
                Request Data Deletion
              </Button>
            </Box>
          </Paper>
          
          <Paper className={classes.paper}>
            <Typography variant="h5" gutterBottom>
              Blockchain Verification Records
            </Typography>
            <Typography variant="body2" color="textSecondary" paragraph>
              Your identity verification history is securely stored on the blockchain.
            </Typography>
            
            <List>
              <ListItem>
                <ListItemIcon>
                  <BlockIcon />
                </ListItemIcon>
                <ListItemText
                  primary="Government ID Verification"
                  secondary="Verified on Oct 15, 2023 | Transaction ID: 0x87c9d..."
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <BlockIcon />
                </ListItemIcon>
                <ListItemText
                  primary="Biometric Verification"
                  secondary="Verified on Oct 15, 2023 | Transaction ID: 0x92a1f..."
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <BlockIcon />
                </ListItemIcon>
                <ListItemText
                  primary="Access Permission Update"
                  secondary="Updated on Oct 16, 2023 | Transaction ID: 0xb78e2..."
                />
              </ListItem>
            </List>
            
            <Box mt={2}>
              <Button variant="outlined" color="primary" size="small">
                View All Blockchain Transactions
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default ProfilePage; 