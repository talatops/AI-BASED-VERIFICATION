import React, { useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Card,
  CardContent,
  CardHeader,
  Divider,
  makeStyles,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  FormControl,
  FormLabel,
  RadioGroup,
  Radio,
  FormControlLabel,
  Chip,
  Snackbar,
  Box,
  Tooltip,
  IconButton,
} from '@material-ui/core';
import MuiAlert from '@material-ui/lab/Alert';
import LockIcon from '@material-ui/icons/Lock';
import EnhancedEncryptionIcon from '@material-ui/icons/EnhancedEncryption';
import InfoIcon from '@material-ui/icons/Info';
import CompareArrowsIcon from '@material-ui/icons/CompareArrows';
import AddIcon from '@material-ui/icons/Add';
import RemoveIcon from '@material-ui/icons/Remove';
import FunctionsIcon from '@material-ui/icons/Functions';
import DoneIcon from '@material-ui/icons/Done';
import CodeIcon from '@material-ui/icons/Code';
import { privacyService } from '../services/api';

const useStyles = makeStyles((theme) => ({
  container: {
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4),
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: theme.spacing(3),
  },
  headerIcon: {
    marginRight: theme.spacing(1),
    color: theme.palette.primary.main,
  },
  paper: {
    padding: theme.spacing(3),
    marginBottom: theme.spacing(3),
  },
  card: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
  },
  cardContent: {
    flexGrow: 1,
  },
  divider: {
    margin: theme.spacing(3, 0),
  },
  demoArea: {
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(2),
    borderRadius: theme.shape.borderRadius,
  },
  result: {
    marginTop: theme.spacing(2),
    padding: theme.spacing(2),
    backgroundColor: theme.palette.success.light,
    borderRadius: theme.shape.borderRadius,
  },
  stepper: {
    backgroundColor: 'transparent',
  },
  infoBox: {
    backgroundColor: theme.palette.info.light,
    padding: theme.spacing(2),
    borderRadius: theme.shape.borderRadius,
    marginBottom: theme.spacing(2),
  },
  codeBlock: {
    backgroundColor: '#f5f5f5',
    padding: theme.spacing(2),
    borderRadius: theme.shape.borderRadius,
    fontFamily: 'monospace',
    whiteSpace: 'pre-wrap',
    overflowX: 'auto',
  },
  actionsContainer: {
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
  },
  loadingContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100px',
  },
  buttonProgress: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    marginTop: -12,
    marginLeft: -12,
  },
  infoIcon: {
    marginLeft: theme.spacing(1),
    fontSize: 18,
    color: theme.palette.info.main,
  },
  operationIcon: {
    marginRight: theme.spacing(1),
  },
  chip: {
    margin: theme.spacing(0.5),
  },
  buttonWrapper: {
    margin: theme.spacing(1),
    position: 'relative',
  },
  encryptedValue: {
    color: theme.palette.primary.main,
    fontWeight: 'bold',
    wordBreak: 'break-all',
  },
}));

// Create custom Alert component
const Alert = (props) => {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
};

const HomomorphicEncryptionPage = () => {
  const classes = useStyles();
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState({
    open: false,
    message: '',
    severity: 'info',
  });

  // Demo state
  const [values, setValues] = useState({ value1: '', value2: '' });
  const [operation, setOperation] = useState('add');
  const [encrypted, setEncrypted] = useState({ value1: '', value2: '', result: '' });
  const [decrypted, setDecrypted] = useState(null);
  const [infoExpanded, setInfoExpanded] = useState(false);

  const handleValueChange = (e) => {
    const { name, value } = e.target;
    setValues({ ...values, [name]: value });
  };

  const handleOperationChange = (e) => {
    setOperation(e.target.value);
  };

  const toggleInfo = () => {
    setInfoExpanded(!infoExpanded);
  };

  const handleEncrypt = async () => {
    setLoading(true);
    try {
      // In a real app, we would encrypt both values with homomorphic encryption
      // For demo purposes, we'll use a mock encrypted value
      const encryptedValue1 = await privacyService.encryptValue(values.value1);
      const encryptedValue2 = await privacyService.encryptValue(values.value2);

      setEncrypted({
        value1: encryptedValue1.data.encrypted_value,
        value2: encryptedValue2.data.encrypted_value,
        result: '',
      });

      setNotification({
        open: true,
        message: 'Values encrypted successfully!',
        severity: 'success',
      });

      setActiveStep(1);
    } catch (error) {
      console.error('Error encrypting values:', error);
      setNotification({
        open: true,
        message: 'Failed to encrypt values: ' + (error.response?.data?.detail || error.message),
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCompute = async () => {
    setLoading(true);
    try {
      // In a real app, we would perform homomorphic operations
      const computeResponse = await privacyService.computeOnEncryptedData({
        encrypted_value1: encrypted.value1,
        encrypted_value2: encrypted.value2,
        operation: operation,
      });

      setEncrypted({
        ...encrypted,
        result: computeResponse.data.encrypted_result,
      });

      setNotification({
        open: true,
        message: 'Computation performed successfully!',
        severity: 'success',
      });

      setActiveStep(2);
    } catch (error) {
      console.error('Error computing with encrypted values:', error);
      setNotification({
        open: true,
        message: 'Failed to compute: ' + (error.response?.data?.detail || error.message),
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDecrypt = async () => {
    setLoading(true);
    try {
      // In a real app, we would decrypt the result
      const decryptResponse = await privacyService.decryptValue(encrypted.result);

      setDecrypted(decryptResponse.data.decrypted_value);

      setNotification({
        open: true,
        message: 'Result decrypted successfully!',
        severity: 'success',
      });

      setActiveStep(3);
    } catch (error) {
      console.error('Error decrypting result:', error);
      setNotification({
        open: true,
        message: 'Failed to decrypt: ' + (error.response?.data?.detail || error.message),
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setValues({ value1: '', value2: '' });
    setEncrypted({ value1: '', value2: '', result: '' });
    setDecrypted(null);
    setActiveStep(0);
  };

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleCloseNotification = () => {
    setNotification({ ...notification, open: false });
  };

  const getOperationIcon = () => {
    switch (operation) {
      case 'add':
        return <AddIcon className={classes.operationIcon} />;
      case 'subtract':
        return <RemoveIcon className={classes.operationIcon} />;
      case 'multiply':
        return <FunctionsIcon className={classes.operationIcon} />;
      default:
        return null;
    }
  };

  const getSteps = () => [
    'Encrypt Your Values',
    'Perform Computation',
    'Get Encrypted Result',
    'Decrypt Result',
  ];

  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <>
            <Typography variant="subtitle1">Enter two numeric values to encrypt:</Typography>
            <Grid container spacing={2} style={{ marginTop: '10px' }}>
              <Grid item xs={12} sm={6}>
                <TextField
                  name="value1"
                  label="First Value"
                  variant="outlined"
                  fullWidth
                  type="number"
                  value={values.value1}
                  onChange={handleValueChange}
                  disabled={loading}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  name="value2"
                  label="Second Value"
                  variant="outlined"
                  fullWidth
                  type="number"
                  value={values.value2}
                  onChange={handleValueChange}
                  disabled={loading}
                />
              </Grid>
            </Grid>
            <div className={classes.actionsContainer}>
              <div>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleEncrypt}
                  disabled={loading || !values.value1 || !values.value2}
                  className={classes.button}
                >
                  {loading ? <CircularProgress size={24} className={classes.buttonProgress} /> : 'Encrypt Values'}
                </Button>
              </div>
            </div>
          </>
        );
      case 1:
        return (
          <>
            <Typography variant="subtitle1" gutterBottom>
              Your values have been encrypted. Now choose an operation:
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <FormControl component="fieldset">
                  <RadioGroup
                    row
                    name="operation"
                    value={operation}
                    onChange={handleOperationChange}
                  >
                    <FormControlLabel
                      value="add"
                      control={<Radio color="primary" />}
                      label={
                        <Box display="flex" alignItems="center">
                          <AddIcon className={classes.operationIcon} />
                          Addition
                        </Box>
                      }
                      disabled={loading}
                    />
                    <FormControlLabel
                      value="subtract"
                      control={<Radio color="primary" />}
                      label={
                        <Box display="flex" alignItems="center">
                          <RemoveIcon className={classes.operationIcon} />
                          Subtraction
                        </Box>
                      }
                      disabled={loading}
                    />
                    <FormControlLabel
                      value="multiply"
                      control={<Radio color="primary" />}
                      label={
                        <Box display="flex" alignItems="center">
                          <FunctionsIcon className={classes.operationIcon} />
                          Multiplication
                        </Box>
                      }
                      disabled={loading}
                    />
                  </RadioGroup>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <Card>
                  <CardContent>
                    <Typography variant="subtitle2" gutterBottom>
                      Encrypted Value 1:
                    </Typography>
                    <Typography variant="body2" className={classes.encryptedValue}>
                      {encrypted.value1.substring(0, 50)}...
                    </Typography>
                    <Divider style={{ margin: '10px 0' }} />
                    <Typography variant="subtitle2" gutterBottom>
                      Encrypted Value 2:
                    </Typography>
                    <Typography variant="body2" className={classes.encryptedValue}>
                      {encrypted.value2.substring(0, 50)}...
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
            <div className={classes.actionsContainer}>
              <Grid container spacing={2}>
                <Grid item>
                  <Button
                    disabled={activeStep === 0 || loading}
                    onClick={handleBack}
                    className={classes.button}
                  >
                    Back
                  </Button>
                </Grid>
                <Grid item>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleCompute}
                    className={classes.button}
                    disabled={loading}
                  >
                    {loading ? <CircularProgress size={24} className={classes.buttonProgress} /> : 'Compute'}
                  </Button>
                </Grid>
              </Grid>
            </div>
          </>
        );
      case 2:
        return (
          <>
            <Typography variant="subtitle1" gutterBottom>
              Computation completed on encrypted values. The server performed {operation}ition without seeing the actual values.
            </Typography>
            <Card>
              <CardContent>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <Box display="flex" alignItems="center">
                      <Typography variant="subtitle2" style={{ marginRight: '10px' }}>
                        Operation:
                      </Typography>
                      <Chip
                        icon={getOperationIcon()}
                        label={operation.charAt(0).toUpperCase() + operation.slice(1)}
                        color="primary"
                        className={classes.chip}
                      />
                    </Box>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="subtitle2" gutterBottom>
                      Encrypted Result:
                    </Typography>
                    <Typography variant="body2" className={classes.encryptedValue}>
                      {encrypted.result.substring(0, 50)}...
                    </Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
            <div className={classes.actionsContainer}>
              <Grid container spacing={2}>
                <Grid item>
                  <Button
                    disabled={activeStep === 0 || loading}
                    onClick={handleBack}
                    className={classes.button}
                  >
                    Back
                  </Button>
                </Grid>
                <Grid item>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleDecrypt}
                    className={classes.button}
                    disabled={loading}
                  >
                    {loading ? <CircularProgress size={24} className={classes.buttonProgress} /> : 'Decrypt Result'}
                  </Button>
                </Grid>
              </Grid>
            </div>
          </>
        );
      case 3:
        return (
          <>
            <Typography variant="subtitle1" gutterBottom>
              The result has been decrypted. Here's your computation:
            </Typography>
            <Box className={classes.result}>
              <Typography variant="h6" align="center">
                {values.value1} {operation === 'add' ? '+' : operation === 'subtract' ? '-' : '×'} {values.value2} = {decrypted}
              </Typography>
            </Box>
            <div className={classes.actionsContainer}>
              <Grid container spacing={2}>
                <Grid item>
                  <Button
                    disabled={activeStep === 0 || loading}
                    onClick={handleBack}
                    className={classes.button}
                  >
                    Back
                  </Button>
                </Grid>
                <Grid item>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleReset}
                    className={classes.button}
                  >
                    Try Again
                  </Button>
                </Grid>
              </Grid>
            </div>
          </>
        );
      default:
        return 'Unknown step';
    }
  };

  return (
    <Container className={classes.container}>
      <div className={classes.header}>
        <EnhancedEncryptionIcon className={classes.headerIcon} fontSize="large" />
        <Typography variant="h4" component="h1">
          Homomorphic Encryption
        </Typography>
      </div>

      <Typography variant="body1" paragraph>
        Experience privacy-preserving computation with homomorphic encryption, allowing calculations on encrypted data without decryption.
      </Typography>

      <Paper className={classes.paper}>
        <Box display="flex" alignItems="center" mb={1}>
          <Typography variant="h6">
            How It Works
          </Typography>
          <IconButton size="small" onClick={toggleInfo}>
            <InfoIcon className={classes.infoIcon} />
          </IconButton>
        </Box>

        {infoExpanded && (
          <Paper className={classes.infoBox}>
            <Typography variant="subtitle1" gutterBottom>
              <strong>What is Homomorphic Encryption?</strong>
            </Typography>
            <Typography variant="body2" paragraph>
              Homomorphic encryption is a type of encryption that allows computations to be performed on encrypted data without decrypting it first. The result, when decrypted, matches the result of operations performed on the plaintext.
            </Typography>
            
            <Typography variant="subtitle2" gutterBottom>
              <strong>Privacy Benefits:</strong>
            </Typography>
            <List dense>
              <ListItem>
                <ListItemIcon>
                  <DoneIcon color="primary" />
                </ListItemIcon>
                <ListItemText primary="Process sensitive data without exposing the actual values" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <DoneIcon color="primary" />
                </ListItemIcon>
                <ListItemText primary="Keep your personal information private while still using online services" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <DoneIcon color="primary" />
                </ListItemIcon>
                <ListItemText primary="Enable secure collaboration without sharing raw data" />
              </ListItem>
            </List>
            
            <Typography variant="subtitle2" gutterBottom>
              <strong>Example Code (Python using SEAL):</strong>
            </Typography>
            <Box className={classes.codeBlock}>
{`# Encrypting and computing homomorphically
from seal import *

# Create encryption context
context = SEALContext(parms)
encryptor = Encryptor(context, public_key)
evaluator = Evaluator(context)
decryptor = Decryptor(context, secret_key)

# Encrypt values
encrypted1 = encryptor.encrypt(encoder.encode(5))
encrypted2 = encryptor.encrypt(encoder.encode(3))

# Perform computation on encrypted data
result = evaluator.add(encrypted1, encrypted2)

# Decrypt result
decrypted = decryptor.decrypt(result)
plaintext = encoder.decode(decrypted)  # Will be 8`}
            </Box>
          </Paper>
        )}

        <Typography variant="subtitle1" gutterBottom>
          Try a demonstration of homomorphic encryption below:
        </Typography>

        <Stepper activeStep={activeStep} orientation="vertical" className={classes.stepper}>
          {getSteps().map((label, index) => (
            <Step key={label}>
              <StepLabel>
                <Typography variant="subtitle1">{label}</Typography>
              </StepLabel>
              <StepContent>
                {getStepContent(index)}
              </StepContent>
            </Step>
          ))}
        </Stepper>
      </Paper>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card className={classes.card}>
            <CardHeader
              title="Use Cases"
              titleTypographyProps={{ variant: 'h6' }}
            />
            <CardContent className={classes.cardContent}>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <LockIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Private Financial Calculations" 
                    secondary="Perform calculations on financial data without revealing sensitive information" 
                  />
                </ListItem>
                <Divider component="li" />
                <ListItem>
                  <ListItemIcon>
                    <LockIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Secure Medical Research" 
                    secondary="Analyze encrypted medical data while preserving patient privacy" 
                  />
                </ListItem>
                <Divider component="li" />
                <ListItem>
                  <ListItemIcon>
                    <LockIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Private Machine Learning" 
                    secondary="Train models on encrypted data without seeing the underlying information" 
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card className={classes.card}>
            <CardHeader
              title="Privacy Benefits"
              titleTypographyProps={{ variant: 'h6' }}
            />
            <CardContent className={classes.cardContent}>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <CompareArrowsIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Data Utility Without Exposure" 
                    secondary="Get insights from your data without revealing raw values" 
                  />
                </ListItem>
                <Divider component="li" />
                <ListItem>
                  <ListItemIcon>
                    <CompareArrowsIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Third-Party Processing" 
                    secondary="Allow third parties to process your data while keeping it encrypted" 
                  />
                </ListItem>
                <Divider component="li" />
                <ListItem>
                  <ListItemIcon>
                    <CompareArrowsIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Regulatory Compliance" 
                    secondary="Help meet privacy regulations like GDPR while still utilizing data" 
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

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

export default HomomorphicEncryptionPage; 