import React, { useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  Stepper,
  Step,
  StepLabel,
  Button,
  makeStyles,
  Grid,
  Card,
  CardContent,
  TextField,
  IconButton,
} from '@material-ui/core';
import PhotoCamera from '@material-ui/icons/PhotoCamera';
import FaceIcon from '@material-ui/icons/Face';
import FingerprintIcon from '@material-ui/icons/Fingerprint';
import DescriptionIcon from '@material-ui/icons/Description';
import DoneIcon from '@material-ui/icons/Done';

const useStyles = makeStyles((theme) => ({
  container: {
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4),
  },
  paper: {
    padding: theme.spacing(3),
    marginBottom: theme.spacing(3),
  },
  stepper: {
    padding: theme.spacing(3, 0, 5),
  },
  buttons: {
    display: 'flex',
    justifyContent: 'flex-end',
    marginTop: theme.spacing(3),
  },
  button: {
    marginLeft: theme.spacing(1),
  },
  icon: {
    fontSize: 48,
    color: theme.palette.primary.main,
    marginBottom: theme.spacing(2),
  },
  uploadButton: {
    marginTop: theme.spacing(2),
  },
  input: {
    display: 'none',
  },
  preview: {
    width: '100%',
    height: 300,
    objectFit: 'cover',
    marginTop: theme.spacing(2),
    border: `1px solid ${theme.palette.grey[300]}`,
    borderRadius: theme.shape.borderRadius,
  },
  successIcon: {
    fontSize: 64,
    color: theme.palette.success.main,
    margin: theme.spacing(2),
  },
}));

const steps = ['Personal Information', 'Government ID', 'Biometric Verification', 'Confirmation'];

function VerificationPage() {
  const classes = useStyles();
  const [activeStep, setActiveStep] = useState(0);
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    dateOfBirth: '',
    idType: '',
    idNumber: '',
    idImage: null,
    biometricType: 'face',
    biometricImage: null,
  });
  const [idPreview, setIdPreview] = useState(null);
  const [facePreview, setFacePreview] = useState(null);

  const handleNext = () => {
    setActiveStep(activeStep + 1);
  };

  const handleBack = () => {
    setActiveStep(activeStep - 1);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleIdUpload = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setFormData({ ...formData, idImage: file });
      setIdPreview(URL.createObjectURL(file));
    }
  };

  const handleFaceUpload = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setFormData({ ...formData, biometricImage: file });
      setFacePreview(URL.createObjectURL(file));
    }
  };

  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Personal Information
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                id="firstName"
                name="firstName"
                label="First name"
                fullWidth
                value={formData.firstName}
                onChange={handleInputChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                id="lastName"
                name="lastName"
                label="Last name"
                fullWidth
                value={formData.lastName}
                onChange={handleInputChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                id="dateOfBirth"
                name="dateOfBirth"
                label="Date of Birth"
                type="date"
                fullWidth
                InputLabelProps={{
                  shrink: true,
                }}
                value={formData.dateOfBirth}
                onChange={handleInputChange}
              />
            </Grid>
          </Grid>
        );
      case 1:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Government ID Verification
              </Typography>
              <Typography variant="body1" gutterBottom>
                Please upload a clear photo of your government-issued ID.
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                id="idType"
                name="idType"
                select
                label="ID Type"
                fullWidth
                value={formData.idType}
                onChange={handleInputChange}
                SelectProps={{
                  native: true,
                }}
              >
                <option value="">Select ID Type</option>
                <option value="passport">Passport</option>
                <option value="driverLicense">Driver's License</option>
                <option value="nationalId">National ID Card</option>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                id="idNumber"
                name="idNumber"
                label="ID Number"
                fullWidth
                value={formData.idNumber}
                onChange={handleInputChange}
              />
            </Grid>
            <Grid item xs={12}>
              <input
                accept="image/*"
                className={classes.input}
                id="id-upload"
                type="file"
                onChange={handleIdUpload}
              />
              <label htmlFor="id-upload">
                <Button
                  variant="contained"
                  color="primary"
                  component="span"
                  className={classes.uploadButton}
                  startIcon={<PhotoCamera />}
                >
                  Upload ID Photo
                </Button>
              </label>
              {idPreview && <img src={idPreview} alt="ID Preview" className={classes.preview} />}
            </Grid>
          </Grid>
        );
      case 2:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Biometric Verification
              </Typography>
              <Typography variant="body1" gutterBottom>
                Please take a clear selfie to verify your identity.
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                id="biometricType"
                name="biometricType"
                select
                label="Biometric Type"
                fullWidth
                value={formData.biometricType}
                onChange={handleInputChange}
                SelectProps={{
                  native: true,
                }}
              >
                <option value="face">Facial Recognition</option>
                <option value="fingerprint">Fingerprint (if available)</option>
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <input
                accept="image/*"
                className={classes.input}
                id="face-upload"
                type="file"
                onChange={handleFaceUpload}
              />
              <label htmlFor="face-upload">
                <Button
                  variant="contained"
                  color="primary"
                  component="span"
                  className={classes.uploadButton}
                  startIcon={<PhotoCamera />}
                >
                  Take Selfie / Upload Biometric
                </Button>
              </label>
              {facePreview && <img src={facePreview} alt="Biometric Preview" className={classes.preview} />}
            </Grid>
          </Grid>
        );
      case 3:
        return (
          <Grid container spacing={3} justify="center" alignItems="center" direction="column">
            <Grid item>
              <DoneIcon className={classes.successIcon} />
            </Grid>
            <Grid item>
              <Typography variant="h5" gutterBottom align="center">
                Verification Completed Successfully
              </Typography>
              <Typography variant="body1" gutterBottom align="center">
                Your identity has been verified and securely stored on the blockchain.
                You now have complete control over who can access your identity data.
              </Typography>
            </Grid>
          </Grid>
        );
      default:
        return 'Unknown step';
    }
  };

  return (
    <Container maxWidth="md" className={classes.container}>
      <Paper className={classes.paper}>
        <Typography component="h1" variant="h4" align="center" gutterBottom>
          Identity Verification
        </Typography>
        <Stepper activeStep={activeStep} className={classes.stepper}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
        {getStepContent(activeStep)}
        <div className={classes.buttons}>
          {activeStep !== 0 && (
            <Button onClick={handleBack} className={classes.button}>
              Back
            </Button>
          )}
          <Button
            variant="contained"
            color="primary"
            onClick={handleNext}
            className={classes.button}
            disabled={activeStep === steps.length - 1}
          >
            {activeStep === steps.length - 2 ? 'Submit Verification' : 'Next'}
          </Button>
        </div>
      </Paper>

      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <DescriptionIcon className={classes.icon} />
              <Typography variant="h6" gutterBottom>
                Government ID
              </Typography>
              <Typography variant="body2">
                We verify the authenticity of your government-issued ID using OCR
                and AI-based validation. Your data is stored encrypted.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <FaceIcon className={classes.icon} />
              <Typography variant="h6" gutterBottom>
                Facial Recognition
              </Typography>
              <Typography variant="body2">
                Our AI compares your selfie with your ID photo to confirm your
                identity, using advanced liveness detection to prevent fraud.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <FingerprintIcon className={classes.icon} />
              <Typography variant="h6" gutterBottom>
                Secure Storage
              </Typography>
              <Typography variant="body2">
                Your verified identity is securely stored on the blockchain with
                zero-knowledge proofs, allowing verification without revealing data.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
}

export default VerificationPage; 