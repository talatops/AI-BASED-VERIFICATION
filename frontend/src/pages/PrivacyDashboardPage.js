import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import {
  Container,
  Typography,
  Grid,
  Paper,
  Divider,
  Box,
  Card,
  CardContent,
  CardHeader,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Chip,
  Button,
  makeStyles,
  CircularProgress,
  Tabs,
  Tab,
  IconButton,
  Tooltip,
  Snackbar,
} from '@material-ui/core';
import MuiAlert from '@material-ui/lab/Alert';
import { styled } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import VerifiedUserIcon from '@material-ui/icons/VerifiedUser';
import SecurityIcon from '@material-ui/icons/Security';
import HistoryIcon from '@material-ui/icons/History';
import InfoIcon from '@material-ui/icons/Info';
import PolicyIcon from '@material-ui/icons/Policy';
import AccessTimeIcon from '@material-ui/icons/AccessTime';
import GetAppIcon from '@material-ui/icons/GetApp';
import LockIcon from '@mui/icons-material/Lock';
import AssignmentIcon from '@mui/icons-material/Assignment';
import DataUsageIcon from '@mui/icons-material/DataUsage';
import FingerprintIcon from '@mui/icons-material/Fingerprint';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import StorageIcon from '@mui/icons-material/Storage';
import CalculateIcon from '@mui/icons-material/Calculate';
import axios from 'axios';
import { gdprService } from '../services/api';
// Replace the import with a mock context
// import { useAuth } from '../contexts/AuthContext';
// Create a mock auth context
const useAuth = () => {
  return {
    currentUser: { uid: 'test-user-id' }
  };
};

const useStyles = makeStyles((theme) => ({
  container: {
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4),
  },
  title: {
    marginBottom: theme.spacing(3),
  },
  paper: {
    padding: theme.spacing(3),
    marginBottom: theme.spacing(3),
  },
  divider: {
    margin: theme.spacing(3, 0),
  },
  loadingContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '50vh',
  },
  card: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
  },
  cardContent: {
    flexGrow: 1,
  },
  tabs: {
    marginBottom: theme.spacing(3),
  },
  chip: {
    margin: theme.spacing(0.5),
  },
  activeChip: {
    backgroundColor: theme.palette.success.main,
    color: theme.palette.common.white,
  },
  expiredChip: {
    backgroundColor: theme.palette.error.main,
    color: theme.palette.common.white,
  },
  categoryChip: {
    margin: theme.spacing(0.5),
    backgroundColor: theme.palette.primary.light,
  },
  statsCard: {
    backgroundColor: theme.palette.grey[100],
  },
  actionButton: {
    marginTop: theme.spacing(2),
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: theme.spacing(2),
  },
  headerIcon: {
    marginRight: theme.spacing(1),
    color: theme.palette.primary.main,
  },
  dataItem: {
    padding: theme.spacing(1),
    borderBottom: `1px solid ${theme.palette.divider}`,
  },
  dataAccessItem: {
    padding: theme.spacing(1),
    borderLeft: `3px solid ${theme.palette.primary.main}`,
    marginBottom: theme.spacing(1),
    backgroundColor: theme.palette.background.default,
  },
  consentCard: {
    marginBottom: theme.spacing(2),
  },
  noDataMessage: {
    textAlign: 'center',
    padding: theme.spacing(3),
  },
}));

// Create a custom Alert component based on MuiAlert
const Alert = (props) => {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
};

const TabPanel = (props) => {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`privacy-tabpanel-${index}`}
      aria-labelledby={`privacy-tab-${index}`}
      {...other}
    >
      {value === index && <Box p={3}>{children}</Box>}
    </div>
  );
};

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(3),
  color: theme.palette.text.primary,
  height: '100%',
}));

const StyledCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
  '&:hover': {
    transform: 'translateY(-5px)',
    boxShadow: theme.shadows[8],
  },
}));

const privacyFeatures = [
  {
    title: 'Biometric Verification',
    description: 'Advanced facial recognition with liveness detection',
    icon: <FingerprintIcon />,
    path: '/verification/face',
    color: '#4CAF50'
  },
  {
    title: 'Document Verification',
    description: 'Secure ID document verification with fraud detection',
    icon: <AssignmentIcon />,
    path: '/verification/document',
    color: '#2196F3'
  },
  {
    title: 'Zero-Knowledge Proofs',
    description: 'Verify without revealing sensitive data',
    icon: <VisibilityOffIcon />,
    path: '/verification/zkp',
    color: '#9C27B0'
  },
  {
    title: 'Homomorphic Encryption',
    description: 'Compute on encrypted data without decryption',
    icon: <CalculateIcon />,
    path: '/privacy/homomorphic-encryption',
    color: '#FF9800'
  },
  {
    title: 'GDPR Compliance',
    description: 'Submit data access, deletion and portability requests',
    icon: <StorageIcon />,
    path: '/privacy/gdpr-requests',
    color: '#E91E63'
  },
  {
    title: 'Permission Management',
    description: 'Control third-party access to your data',
    icon: <LockIcon />,
    path: '/permissions',
    color: '#673AB7'
  }
];

const PrivacyDashboardPage = () => {
  const classes = useStyles();
  const { currentUser } = useAuth();
  const userId = currentUser?.uid || 'test-user-id'; // Fallback for development
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(true);
  const [tabValue, setTabValue] = useState(0);
  const [privacyReport, setPrivacyReport] = useState(null);
  const [notification, setNotification] = useState({
    open: false,
    message: '',
    severity: 'info',
  });
  const [error, setError] = useState(null);
  const [privacySettings, setPrivacySettings] = useState({
    dataCollection: true,
    thirdPartySharing: false,
    behavioralAnalytics: true,
    enhancedPrivacy: false,
    storageEncryption: true,
    twoFactorAuth: false
  });
  const [privacyScore, setPrivacyScore] = useState(75);
  const [verificationStatus, setVerificationStatus] = useState({
    face: 'verified',
    document: 'verified',
    address: 'pending'
  });

  useEffect(() => {
    fetchPrivacyReport();
    fetchPrivacyData();
  }, [userId]);

  const fetchPrivacyReport = async () => {
    setLoading(true);
    try {
      const response = await gdprService.generatePrivacyReport(userId);
      setPrivacyReport(response.data);
    } catch (error) {
      console.error('Error fetching privacy report:', error);
      setNotification({
        open: true,
        message: 'Failed to load privacy report: ' + (error.response?.data?.detail || error.message),
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchPrivacyData = async () => {
    setLoading(true);
    try {
      // In a production app, these would be real API calls
      // const settingsResponse = await axios.get('/api/privacy/settings');
      // const scoreResponse = await axios.get('/api/privacy/score');
      // const verificationResponse = await axios.get('/api/verification/status');
      
      // setPrivacySettings(settingsResponse.data);
      // setPrivacyScore(scoreResponse.data.score);
      // setVerificationStatus(verificationResponse.data);
      
      // Using mock data for now
      setTimeout(() => {
        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching privacy data:', error);
      setError('Failed to load privacy data. Please try again later.');
      setLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const formatDate = (dateString) => {
    try {
      return format(new Date(dateString), 'PPP p');
    } catch (error) {
      return 'Invalid date';
    }
  };

  const handleCloseNotification = () => {
    setNotification({ ...notification, open: false });
  };

  const downloadPrivacyReport = () => {
    if (!privacyReport) return;
    
    // Convert the privacy report to a downloadable JSON file
    const dataStr = JSON.stringify(privacyReport, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `privacy-report-${new Date().toISOString().slice(0, 10)}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
    
    setNotification({
      open: true,
      message: 'Privacy report downloaded successfully',
      severity: 'success',
    });
  };

  const handleSettingChange = async (setting) => {
    const newSettings = {
      ...privacySettings,
      [setting]: !privacySettings[setting]
    };
    
    setPrivacySettings(newSettings);
    
    try {
      // In a production app, this would be a real API call
      // await axios.put('/api/privacy/settings', newSettings);
      
      // Calculate new privacy score based on settings
      const enabledSettings = Object.values(newSettings).filter(Boolean).length;
      const newScore = Math.round((enabledSettings / Object.keys(newSettings).length) * 100);
      setPrivacyScore(newScore);
    } catch (error) {
      console.error('Error updating privacy settings:', error);
      setError('Failed to update privacy settings. Please try again.');
      // Revert the setting change
      setPrivacySettings(privacySettings);
    }
  };

  const navigateToFeature = (path) => {
    navigate(path);
  };

  if (loading) {
    return (
      <Container className={classes.container}>
        <div className={classes.loadingContainer}>
          <CircularProgress />
          <Typography variant="h6" style={{ marginLeft: 20 }}>
            Loading privacy report...
          </Typography>
        </div>
      </Container>
    );
  }

  return (
    <Container className={classes.container}>
      <div className={classes.header}>
        <SecurityIcon className={classes.headerIcon} fontSize="large" />
        <Typography variant="h4" component="h1" className={classes.title}>
          Privacy Dashboard
        </Typography>
        {privacyReport && (
          <Tooltip title="Download Privacy Report">
            <IconButton color="primary" onClick={downloadPrivacyReport}>
              <GetAppIcon />
            </IconButton>
          </Tooltip>
        )}
      </div>

      <Typography variant="body1" paragraph>
        Monitor and manage your privacy settings, consents, and data access history.
        This dashboard provides transparency about how your data is being used.
      </Typography>

      <Paper className={classes.paper}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
          className={classes.tabs}
        >
          <Tab label="Overview" icon={<InfoIcon />} />
          <Tab label="Consents" icon={<PolicyIcon />} />
          <Tab label="Data Access" icon={<HistoryIcon />} />
          <Tab label="GDPR Requests" icon={<VerifiedUserIcon />} />
        </Tabs>

        {!privacyReport ? (
          <div className={classes.noDataMessage}>
            <Typography variant="body1">
              No privacy data available. Please verify your identity first.
            </Typography>
          </div>
        ) : (
          <>
            <TabPanel value={tabValue} index={0}>
              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <Card className={`${classes.card} ${classes.statsCard}`}>
                    <CardHeader title="Active Consents" />
                    <CardContent>
                      <Typography variant="h3" component="p" align="center">
                        {privacyReport.active_consents?.length || 0}
                      </Typography>
                      <Typography variant="body2" align="center">
                        Companies with authorized access to your data
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12} md={4}>
                  <Card className={`${classes.card} ${classes.statsCard}`}>
                    <CardHeader title="Data Categories" />
                    <CardContent>
                      <Typography variant="h3" component="p" align="center">
                        {privacyReport.data_categories_accessed?.length || 0}
                      </Typography>
                      <Typography variant="body2" align="center">
                        Types of data accessed
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12} md={4}>
                  <Card className={`${classes.card} ${classes.statsCard}`}>
                    <CardHeader title="Third Parties" />
                    <CardContent>
                      <Typography variant="h3" component="p" align="center">
                        {privacyReport.third_parties_with_access?.length || 0}
                      </Typography>
                      <Typography variant="body2" align="center">
                        Services with access to your data
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12}>
                  <Card>
                    <CardHeader title="Data Categories Accessed" />
                    <CardContent>
                      <div>
                        {privacyReport.data_categories_accessed?.length > 0 ? (
                          privacyReport.data_categories_accessed.map((category) => (
                            <Chip 
                              key={category} 
                              label={category} 
                              className={classes.categoryChip}
                            />
                          ))
                        ) : (
                          <Typography variant="body2">No data categories have been accessed yet.</Typography>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardHeader title="Recent Data Access" />
                    <CardContent>
                      {privacyReport.recent_data_access?.length > 0 ? (
                        <List>
                          {privacyReport.recent_data_access.slice(0, 5).map((access) => (
                            <div key={access.log_id} className={classes.dataAccessItem}>
                              <Typography variant="subtitle2">
                                {access.data_category} - {access.access_type}
                              </Typography>
                              <Typography variant="body2" color="textSecondary">
                                By: {access.accessed_by} | Purpose: {access.purpose}
                              </Typography>
                              <Typography variant="caption" color="textSecondary">
                                {formatDate(access.timestamp)}
                              </Typography>
                            </div>
                          ))}
                        </List>
                      ) : (
                        <Typography variant="body2">No recent data access recorded.</Typography>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardHeader title="Open GDPR Requests" />
                    <CardContent>
                      {privacyReport.open_requests?.length > 0 ? (
                        <List>
                          {privacyReport.open_requests.map((request) => (
                            <ListItem key={request.request_id} divider>
                              <ListItemText
                                primary={`${request.type} Request`}
                                secondary={`Status: ${request.status} | Submitted: ${formatDate(request.submitted_at)}`}
                              />
                              <ListItemSecondaryAction>
                                <Chip 
                                  label={request.status} 
                                  color="primary" 
                                  variant="outlined" 
                                  size="small"
                                />
                              </ListItemSecondaryAction>
                            </ListItem>
                          ))}
                        </List>
                      ) : (
                        <Typography variant="body2">No open GDPR requests.</Typography>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </TabPanel>

            <TabPanel value={tabValue} index={1}>
              <Typography variant="h6" gutterBottom>Active Consents</Typography>
              {privacyReport.active_consents?.length > 0 ? (
                privacyReport.active_consents.map((consent) => (
                  <Card key={consent.consent_id} className={classes.consentCard}>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        {consent.purpose}
                      </Typography>
                      <Typography variant="body2" color="textSecondary" gutterBottom>
                        Granted: {formatDate(consent.granted_at)}
                      </Typography>
                      <Typography variant="body2" color="textSecondary" gutterBottom>
                        Expires: {formatDate(consent.expires_at)}
                      </Typography>
                      <Typography variant="body2" gutterBottom>
                        Data Categories:
                      </Typography>
                      <div>
                        {consent.data_categories.map((category) => (
                          <Chip 
                            key={category} 
                            label={category} 
                            className={classes.chip}
                            size="small"
                          />
                        ))}
                      </div>
                      {consent.third_parties.length > 0 && (
                        <>
                          <Typography variant="body2" gutterBottom style={{marginTop: 8}}>
                            Shared with:
                          </Typography>
                          <div>
                            {consent.third_parties.map((party) => (
                              <Chip 
                                key={party} 
                                label={party} 
                                className={classes.chip}
                                size="small"
                                variant="outlined"
                              />
                            ))}
                          </div>
                        </>
                      )}
                      <Button 
                        color="secondary" 
                        className={classes.actionButton}
                        onClick={() => {
                          // Would call gdprService.withdrawConsent
                          alert('This would withdraw consent in a real implementation');
                        }}
                      >
                        Withdraw Consent
                      </Button>
                    </CardContent>
                  </Card>
                ))
              ) : (
                <Typography variant="body1">No active consents found.</Typography>
              )}

              <Divider className={classes.divider} />

              <Typography variant="h6" gutterBottom>Withdrawn Consents</Typography>
              {privacyReport.withdrawn_consents?.length > 0 ? (
                privacyReport.withdrawn_consents.map((consent) => (
                  <Card key={consent.consent_id} className={classes.consentCard}>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        {consent.purpose}
                      </Typography>
                      <Typography variant="body2" color="textSecondary" gutterBottom>
                        Granted: {formatDate(consent.granted_at)}
                      </Typography>
                      <Typography variant="body2" color="textSecondary" gutterBottom>
                        Withdrawn: {formatDate(consent.withdrawn_at)}
                      </Typography>
                      <Chip 
                        label="Withdrawn" 
                        className={`${classes.chip} ${classes.expiredChip}`}
                      />
                    </CardContent>
                  </Card>
                ))
              ) : (
                <Typography variant="body1">No withdrawn consents.</Typography>
              )}
            </TabPanel>

            <TabPanel value={tabValue} index={2}>
              <Typography variant="h6" gutterBottom>Data Access History</Typography>
              {privacyReport.recent_data_access?.length > 0 ? (
                <List>
                  {privacyReport.recent_data_access.map((access) => (
                    <ListItem key={access.log_id} className={classes.dataItem}>
                      <ListItemText
                        primary={
                          <span>
                            <AccessTimeIcon fontSize="small" style={{verticalAlign: 'middle', marginRight: 8}} />
                            {formatDate(access.timestamp)}
                          </span>
                        }
                        secondary={
                          <>
                            <Typography variant="body2">
                              <strong>Data Category:</strong> {access.data_category}
                            </Typography>
                            <Typography variant="body2">
                              <strong>Access Type:</strong> {access.access_type}
                            </Typography>
                            <Typography variant="body2">
                              <strong>Accessed By:</strong> {access.accessed_by}
                            </Typography>
                            <Typography variant="body2">
                              <strong>Purpose:</strong> {access.purpose}
                            </Typography>
                          </>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body1">No data access history available.</Typography>
              )}
            </TabPanel>

            <TabPanel value={tabValue} index={3}>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>Open Requests</Typography>
                  {privacyReport.open_requests?.length > 0 ? (
                    <List>
                      {privacyReport.open_requests.map((request) => (
                        <ListItem key={request.request_id} divider>
                          <ListItemText
                            primary={`${request.type} Request`}
                            secondary={
                              <>
                                <Typography variant="body2">
                                  Submitted: {formatDate(request.submitted_at)}
                                </Typography>
                                <Typography variant="body2">
                                  Due by: {formatDate(request.due_by)}
                                </Typography>
                                <Typography variant="body2">
                                  Status: {request.status}
                                </Typography>
                              </>
                            }
                          />
                        </ListItem>
                      ))}
                    </List>
                  ) : (
                    <Typography variant="body1">No open GDPR requests.</Typography>
                  )}
                </Grid>

                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>Completed Requests</Typography>
                  {privacyReport.completed_requests?.length > 0 ? (
                    <List>
                      {privacyReport.completed_requests.map((request) => (
                        <ListItem key={request.request_id} divider>
                          <ListItemText
                            primary={`${request.type} Request`}
                            secondary={
                              <>
                                <Typography variant="body2">
                                  Submitted: {formatDate(request.submitted_at)}
                                </Typography>
                                <Typography variant="body2">
                                  Completed: {formatDate(request.updated_at)}
                                </Typography>
                                <Typography variant="body2">
                                  Status: {request.status}
                                </Typography>
                              </>
                            }
                          />
                        </ListItem>
                      ))}
                    </List>
                  ) : (
                    <Typography variant="body1">No completed GDPR requests.</Typography>
                  )}
                </Grid>

                <Grid item xs={12}>
                  <Card>
                    <CardHeader title="Submit New GDPR Request" />
                    <CardContent>
                      <Typography variant="body1" paragraph>
                        You can submit a new GDPR request to exercise your data rights.
                      </Typography>
                      <Button 
                        variant="contained" 
                        color="primary"
                        className={classes.actionButton}
                        onClick={() => {
                          window.location.href = '/gdpr';
                        }}
                      >
                        New GDPR Request
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </TabPanel>
          </>
        )}
      </Paper>

      <Snackbar 
        open={notification.open} 
        autoHideDuration={6000} 
        onClose={handleCloseNotification}
      >
        <Alert onClose={handleCloseNotification} severity={notification.severity}>
          {notification.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default PrivacyDashboardPage; 