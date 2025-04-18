import React, { useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  TextField,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Switch,
  FormControlLabel,
  makeStyles,
  Chip,
  Box,
  Divider,
} from '@material-ui/core';
import BusinessIcon from '@material-ui/icons/Business';
import AddIcon from '@material-ui/icons/Add';
import DeleteIcon from '@material-ui/icons/Delete';
import InfoIcon from '@material-ui/icons/Info';
import BlockIcon from '@material-ui/icons/ViewModule';
import HistoryIcon from '@material-ui/icons/History';
import LockIcon from '@material-ui/icons/Lock';

const useStyles = makeStyles((theme) => ({
  container: {
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4),
  },
  paper: {
    padding: theme.spacing(3),
    marginBottom: theme.spacing(3),
  },
  title: {
    marginBottom: theme.spacing(2),
  },
  permissionCard: {
    marginBottom: theme.spacing(2),
    transition: 'transform 0.2s',
    '&:hover': {
      transform: 'translateY(-4px)',
      boxShadow: theme.shadows[4],
    },
  },
  permissionHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: theme.spacing(2),
  },
  chip: {
    margin: theme.spacing(0.5),
  },
  addButton: {
    marginTop: theme.spacing(2),
  },
  infoIcon: {
    marginLeft: theme.spacing(1),
    color: theme.palette.info.main,
    cursor: 'pointer',
  },
  permissionItem: {
    border: `1px solid ${theme.palette.divider}`,
    borderRadius: theme.shape.borderRadius,
    marginBottom: theme.spacing(2),
    padding: theme.spacing(2),
  },
  activePermission: {
    borderLeft: `4px solid ${theme.palette.success.main}`,
  },
  inactivePermission: {
    borderLeft: `4px solid ${theme.palette.error.main}`,
  },
  dataTypeList: {
    display: 'flex',
    flexWrap: 'wrap',
    margin: theme.spacing(1, 0),
  },
  serviceIcon: {
    backgroundColor: theme.palette.primary.light,
    color: theme.palette.primary.contrastText,
    padding: theme.spacing(1),
    borderRadius: '50%',
    marginRight: theme.spacing(2),
  },
  accessHistory: {
    marginTop: theme.spacing(2),
    padding: theme.spacing(1),
    backgroundColor: theme.palette.background.default,
    borderRadius: theme.shape.borderRadius,
  },
  historyItem: {
    fontSize: '0.875rem',
  },
  blockchainInfo: {
    marginTop: theme.spacing(2),
    padding: theme.spacing(1),
    backgroundColor: theme.palette.grey[100],
    borderRadius: theme.shape.borderRadius,
  },
}));

function PermissionsPage() {
  const classes = useStyles();
  
  // Mock permission data
  const [permissions, setPermissions] = useState([
    {
      id: '1',
      serviceName: 'BankSecure Financial',
      serviceId: 'bank123',
      active: true,
      grantedDate: '2023-09-15T10:30:00Z',
      expiryDate: '2024-03-15T10:30:00Z',
      dataTypes: ['name', 'address', 'dateOfBirth'],
      accessLog: [
        { timestamp: '2023-10-16T14:25:12Z', action: 'Accessed identity verification' },
        { timestamp: '2023-10-02T09:18:45Z', action: 'Accessed identity verification' },
      ],
      zkpEnabled: true,
      blockchainTxId: '0x8d72c3e21a0f4b84a7350a50a722651b49f7b509...',
    },
    {
      id: '2',
      serviceName: 'HealthCare Plus',
      serviceId: 'health456',
      active: true,
      grantedDate: '2023-08-20T15:45:00Z',
      expiryDate: '2023-11-20T15:45:00Z',
      dataTypes: ['name', 'dateOfBirth'],
      accessLog: [
        { timestamp: '2023-10-10T11:05:33Z', action: 'Accessed identity verification' },
      ],
      zkpEnabled: true,
      blockchainTxId: '0x7c91fd3e45b7a8f2e761c9268d0e91ca6d88126c...',
    },
    {
      id: '3',
      serviceName: 'TravelSafe Bookings',
      serviceId: 'travel789',
      active: false,
      grantedDate: '2023-06-10T09:20:00Z',
      expiryDate: '2023-09-10T09:20:00Z',
      dataTypes: ['name', 'address'],
      accessLog: [
        { timestamp: '2023-08-15T16:42:19Z', action: 'Accessed identity verification' },
        { timestamp: '2023-07-22T08:11:05Z', action: 'Accessed identity verification' },
      ],
      zkpEnabled: false,
      blockchainTxId: '0x3a56e7d9f1b5c8e4d2a6b7c8d9e0f1a2b3c4d5e6...',
    },
  ]);
  
  const [openDialog, setOpenDialog] = useState(false);
  const [newService, setNewService] = useState({
    serviceName: '',
    serviceId: '',
    dataTypes: {
      name: true,
      address: false,
      phone: false,
      email: false,
      dateOfBirth: false,
    },
    zkpEnabled: true,
  });
  
  const [openInfoDialog, setOpenInfoDialog] = useState(false);
  const [selectedPermission, setSelectedPermission] = useState(null);

  const handleOpenDialog = () => {
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };
  
  const handleOpenInfoDialog = (permission) => {
    setSelectedPermission(permission);
    setOpenInfoDialog(true);
  };
  
  const handleCloseInfoDialog = () => {
    setOpenInfoDialog(false);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewService({ ...newService, [name]: value });
  };

  const handleDataTypeChange = (event) => {
    setNewService({
      ...newService,
      dataTypes: {
        ...newService.dataTypes,
        [event.target.name]: event.target.checked,
      },
    });
  };
  
  const handleZkpChange = (event) => {
    setNewService({
      ...newService,
      zkpEnabled: event.target.checked,
    });
  };

  const handleAddService = () => {
    // In a real app, this would call an API to update blockchain permissions
    const selectedDataTypes = Object.keys(newService.dataTypes).filter(
      (key) => newService.dataTypes[key]
    );
    
    const newPermission = {
      id: (permissions.length + 1).toString(),
      serviceName: newService.serviceName,
      serviceId: newService.serviceId,
      active: true,
      grantedDate: new Date().toISOString(),
      expiryDate: new Date(Date.now() + 6 * 30 * 24 * 60 * 60 * 1000).toISOString(),
      dataTypes: selectedDataTypes,
      accessLog: [],
      zkpEnabled: newService.zkpEnabled,
      blockchainTxId: '0x' + Math.random().toString(16).substr(2, 40) + '...',
    };
    
    setPermissions([...permissions, newPermission]);
    setNewService({
      serviceName: '',
      serviceId: '',
      dataTypes: {
        name: true,
        address: false,
        phone: false,
        email: false,
        dateOfBirth: false,
      },
      zkpEnabled: true,
    });
    handleCloseDialog();
  };

  const handleTogglePermission = (id) => {
    setPermissions(
      permissions.map((perm) =>
        perm.id === id ? { ...perm, active: !perm.active } : perm
      )
    );
  };

  const handleRevokePermission = (id) => {
    setPermissions(permissions.filter((perm) => perm.id !== id));
  };

  return (
    <Container maxWidth="lg" className={classes.container}>
      <Paper className={classes.paper}>
        <div className={classes.permissionHeader}>
          <Typography variant="h4" component="h1" className={classes.title}>
            Identity Data Permissions
          </Typography>
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={handleOpenDialog}
          >
            Grant New Permission
          </Button>
        </div>
        
        <Typography variant="body1" paragraph>
          Control which services can access your verified identity data. 
          All permissions are securely recorded on the blockchain with your consent.
        </Typography>
        
        <Typography variant="h6" gutterBottom>
          Active Permissions
        </Typography>
        
        {permissions.length === 0 ? (
          <Typography variant="body2">No permissions granted yet.</Typography>
        ) : (
          permissions.map((permission) => (
            <div 
              key={permission.id} 
              className={`${classes.permissionItem} ${
                permission.active 
                  ? classes.activePermission 
                  : classes.inactivePermission
              }`}
            >
              <Grid container alignItems="center">
                <Grid item>
                  <BusinessIcon className={classes.serviceIcon} />
                </Grid>
                <Grid item xs>
                  <Typography variant="h6">{permission.serviceName}</Typography>
                  <Typography variant="body2" color="textSecondary">
                    Service ID: {permission.serviceId}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {permission.active ? 'Active' : 'Inactive'} • Granted: {new Date(permission.grantedDate).toLocaleDateString()} • 
                    Expires: {new Date(permission.expiryDate).toLocaleDateString()}
                  </Typography>
                  
                  <div className={classes.dataTypeList}>
                    {permission.dataTypes.map((type) => (
                      <Chip
                        key={type}
                        label={type}
                        size="small"
                        className={classes.chip}
                      />
                    ))}
                    {permission.zkpEnabled && (
                      <Chip
                        icon={<LockIcon />}
                        label="Zero-Knowledge Proof"
                        size="small"
                        color="secondary"
                        className={classes.chip}
                      />
                    )}
                  </div>
                  
                  <div className={classes.blockchainInfo}>
                    <Typography variant="body2" display="flex" alignItems="center">
                      <BlockIcon fontSize="small" style={{ marginRight: 8 }} />
                      Blockchain Transaction: {permission.blockchainTxId}
                    </Typography>
                  </div>
                  
                  {permission.accessLog.length > 0 && (
                    <div className={classes.accessHistory}>
                      <Typography variant="body2" display="flex" alignItems="center">
                        <HistoryIcon fontSize="small" style={{ marginRight: 8 }} />
                        Recent access:
                      </Typography>
                      {permission.accessLog.slice(0, 1).map((log, index) => (
                        <Typography key={index} variant="body2" className={classes.historyItem}>
                          {new Date(log.timestamp).toLocaleString()} - {log.action}
                        </Typography>
                      ))}
                    </div>
                  )}
                </Grid>
                
                <Grid item>
                  <IconButton 
                    size="small" 
                    onClick={() => handleOpenInfoDialog(permission)}
                    aria-label="view details"
                  >
                    <InfoIcon />
                  </IconButton>
                </Grid>
                
                <Grid item>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={permission.active}
                        onChange={() => handleTogglePermission(permission.id)}
                        color="primary"
                      />
                    }
                    label={permission.active ? "Enabled" : "Disabled"}
                  />
                </Grid>
                
                <Grid item>
                  <IconButton 
                    edge="end" 
                    aria-label="revoke" 
                    onClick={() => handleRevokePermission(permission.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Grid>
              </Grid>
            </div>
          ))
        )}
      </Paper>
      
      <Paper className={classes.paper}>
        <Typography variant="h5" gutterBottom>
          About Identity Permissions
        </Typography>
        <Typography variant="body1" paragraph>
          When you grant permission to a service to access your identity data, you can:
        </Typography>
        <List>
          <ListItem>
            <ListItemIcon>
              <LockIcon />
            </ListItemIcon>
            <ListItemText 
              primary="Use Zero-Knowledge Proofs" 
              secondary="Share proof of identity claims without revealing the actual data"
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <BlockIcon />
            </ListItemIcon>
            <ListItemText 
              primary="Blockchain Security" 
              secondary="All permissions are recorded on the blockchain for transparency and security"
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <HistoryIcon />
            </ListItemIcon>
            <ListItemText 
              primary="Access History" 
              secondary="Track when and how services access your identity data"
            />
          </ListItem>
        </List>
      </Paper>
      
      {/* Add Service Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} aria-labelledby="form-dialog-title">
        <DialogTitle id="form-dialog-title">Grant Permission to Service</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Enter the details of the service you want to grant access to your verified identity.
            You can choose which specific data to share.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="serviceName"
            name="serviceName"
            label="Service Name"
            type="text"
            fullWidth
            value={newService.serviceName}
            onChange={handleInputChange}
          />
          <TextField
            margin="dense"
            id="serviceId"
            name="serviceId"
            label="Service ID"
            type="text"
            fullWidth
            value={newService.serviceId}
            onChange={handleInputChange}
          />
          
          <Typography variant="subtitle1" style={{ marginTop: 16 }}>
            Select data to share:
          </Typography>
          
          <FormControlLabel
            control={
              <Switch
                checked={newService.dataTypes.name}
                onChange={handleDataTypeChange}
                name="name"
                color="primary"
              />
            }
            label="Full Name"
          />
          <FormControlLabel
            control={
              <Switch
                checked={newService.dataTypes.address}
                onChange={handleDataTypeChange}
                name="address"
                color="primary"
              />
            }
            label="Address"
          />
          <FormControlLabel
            control={
              <Switch
                checked={newService.dataTypes.phone}
                onChange={handleDataTypeChange}
                name="phone"
                color="primary"
              />
            }
            label="Phone Number"
          />
          <FormControlLabel
            control={
              <Switch
                checked={newService.dataTypes.email}
                onChange={handleDataTypeChange}
                name="email"
                color="primary"
              />
            }
            label="Email Address"
          />
          <FormControlLabel
            control={
              <Switch
                checked={newService.dataTypes.dateOfBirth}
                onChange={handleDataTypeChange}
                name="dateOfBirth"
                color="primary"
              />
            }
            label="Date of Birth"
          />
          
          <Divider style={{ margin: '16px 0' }} />
          
          <FormControlLabel
            control={
              <Switch
                checked={newService.zkpEnabled}
                onChange={handleZkpChange}
                name="zkpEnabled"
                color="secondary"
              />
            }
            label="Enable Zero-Knowledge Proofs (recommended for enhanced privacy)"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} color="primary">
            Cancel
          </Button>
          <Button 
            onClick={handleAddService} 
            color="primary" 
            disabled={!newService.serviceName || !newService.serviceId}
          >
            Grant Permission
          </Button>
        </DialogActions>
      </Dialog>
      
      {/* Permission Info Dialog */}
      <Dialog
        open={openInfoDialog}
        onClose={handleCloseInfoDialog}
        aria-labelledby="info-dialog-title"
        maxWidth="md"
      >
        {selectedPermission && (
          <>
            <DialogTitle id="info-dialog-title">
              {selectedPermission.serviceName} - Access Details
            </DialogTitle>
            <DialogContent>
              <Typography variant="subtitle1" gutterBottom>
                Service Information
              </Typography>
              <Typography variant="body2">
                <strong>Service ID:</strong> {selectedPermission.serviceId}
              </Typography>
              <Typography variant="body2">
                <strong>Status:</strong> {selectedPermission.active ? 'Active' : 'Inactive'}
              </Typography>
              <Typography variant="body2">
                <strong>Granted:</strong> {new Date(selectedPermission.grantedDate).toLocaleString()}
              </Typography>
              <Typography variant="body2">
                <strong>Expires:</strong> {new Date(selectedPermission.expiryDate).toLocaleString()}
              </Typography>
              
              <Typography variant="subtitle1" style={{ marginTop: 16 }} gutterBottom>
                Shared Data Types
              </Typography>
              <div className={classes.dataTypeList}>
                {selectedPermission.dataTypes.map((type) => (
                  <Chip key={type} label={type} className={classes.chip} />
                ))}
              </div>
              
              <Typography variant="subtitle1" style={{ marginTop: 16 }} gutterBottom>
                Security Features
              </Typography>
              <Typography variant="body2">
                <strong>Zero-Knowledge Proofs:</strong> {selectedPermission.zkpEnabled ? 'Enabled' : 'Disabled'}
              </Typography>
              <Typography variant="body2">
                <strong>Blockchain Transaction:</strong> {selectedPermission.blockchainTxId}
              </Typography>
              
              <Typography variant="subtitle1" style={{ marginTop: 16 }} gutterBottom>
                Access History
              </Typography>
              {selectedPermission.accessLog.length === 0 ? (
                <Typography variant="body2">No access recorded yet.</Typography>
              ) : (
                <List dense>
                  {selectedPermission.accessLog.map((log, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <HistoryIcon fontSize="small" />
                      </ListItemIcon>
                      <ListItemText
                        primary={log.action}
                        secondary={new Date(log.timestamp).toLocaleString()}
                      />
                    </ListItem>
                  ))}
                </List>
              )}
            </DialogContent>
            <DialogActions>
              <Button 
                onClick={() => handleRevokePermission(selectedPermission.id)} 
                color="secondary"
              >
                Revoke Access
              </Button>
              <Button onClick={handleCloseInfoDialog} color="primary">
                Close
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Container>
  );
}

export default PermissionsPage;