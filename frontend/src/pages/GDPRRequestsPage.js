import React, { useState, useEffect } from 'react';
import { 
  Container, Typography, Box, Grid, Paper, Button, 
  TextField, MenuItem, Snackbar, Alert, CircularProgress,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { gdprService } from '../services/api';

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(3),
  color: theme.palette.text.primary,
  height: '100%',
}));

const requestTypes = [
  { value: 'access', label: 'Data Access Request' },
  { value: 'deletion', label: 'Data Deletion Request' },
  { value: 'rectification', label: 'Data Rectification Request' },
  { value: 'portability', label: 'Data Portability Request' },
  { value: 'objection', label: 'Processing Objection' },
  { value: 'restriction', label: 'Processing Restriction' },
];

const GDPRRequestsPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [requests, setRequests] = useState([]);
  const [newRequest, setNewRequest] = useState({
    type: 'access',
    description: ''
  });
  const [notification, setNotification] = useState({
    open: false,
    message: '',
    severity: 'success'
  });
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedRequest, setSelectedRequest] = useState(null);
  
  // Mock user ID for demo purposes - in a real app, this would come from authentication
  const userId = "test-user-123";
  
  useEffect(() => {
    if (userId) {
      fetchRequests();
    }
  }, [userId]);

  const fetchRequests = async () => {
    setLoading(true);
    try {
      // Call the GDPR requests endpoint
      const response = await gdprService.getGdprRequests(userId);
      setRequests(response.data);
    } catch (error) {
      console.error('Failed to fetch GDPR requests:', error);
      setNotification({
        open: true,
        message: 'Failed to load your GDPR requests. Please try again.',
        severity: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewRequest(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Submit DSR request
      const response = await gdprService.submitDSR(userId, newRequest.type, { description: newRequest.description });
      setRequests(prev => [...prev, response.data]);
      setNewRequest({
        type: 'access',
        description: ''
      });
      setNotification({
        open: true,
        message: 'Your GDPR request has been submitted successfully!',
        severity: 'success'
      });
    } catch (error) {
      console.error('Failed to submit GDPR request:', error);
      setNotification({
        open: true,
        message: 'Failed to submit your request. Please try again.',
        severity: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCloseNotification = () => {
    setNotification(prev => ({
      ...prev,
      open: false
    }));
  };

  const handleViewDetails = (request) => {
    setSelectedRequest(request);
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedRequest(null);
  };

  const renderRequestStatus = (status) => {
    const statusColors = {
      pending: '#FFC107',
      processing: '#2196F3',
      completed: '#4CAF50',
      rejected: '#F44336'
    };
    
    return (
      <Box
        component="span"
        sx={{
          backgroundColor: statusColors[status] || '#757575',
          color: 'white',
          padding: '3px 10px',
          borderRadius: '12px',
          fontSize: '0.75rem',
          fontWeight: 'bold',
          textTransform: 'uppercase'
        }}
      >
        {status}
      </Box>
    );
  };

  // Mock data for development
  useEffect(() => {
    if (requests.length === 0) {
      setRequests([
        {
          id: '001',
          type: 'access',
          description: 'I would like to receive a copy of all my personal data',
          status: 'completed',
          createdAt: '2023-09-15T10:30:00Z',
          updatedAt: '2023-09-17T14:20:00Z',
          responseData: {
            downloadUrl: 'https://example.com/data/user123.zip',
            expiresAt: '2023-09-24T14:20:00Z'
          }
        },
        {
          id: '002',
          type: 'deletion',
          description: 'Please delete all my account data and personal information',
          status: 'processing',
          createdAt: '2023-09-18T09:45:00Z',
          updatedAt: '2023-09-18T15:10:00Z'
        },
        {
          id: '003',
          type: 'portability',
          description: 'I want to transfer my data to a different service',
          status: 'pending',
          createdAt: '2023-09-19T16:20:00Z',
          updatedAt: '2023-09-19T16:20:00Z'
        }
      ]);
    }
  }, [requests]);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 8 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        GDPR Privacy Requests
      </Typography>
      
      <Box sx={{ mb: 4 }}>
        <Typography variant="body1" color="text.secondary" paragraph>
          Submit requests related to your personal data under GDPR regulations.
          You can request access to your data, correction of inaccurate data, or deletion of your information.
        </Typography>
      </Box>
      
      <Grid container spacing={4}>
        <Grid item xs={12} md={5}>
          <Item>
            <Typography variant="h6" component="h2" gutterBottom>
              Submit a New Request
            </Typography>
            
            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
              <TextField
                select
                fullWidth
                label="Request Type"
                name="type"
                value={newRequest.type}
                onChange={handleInputChange}
                margin="normal"
                required
              >
                {requestTypes.map(option => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
              
              <TextField
                fullWidth
                label="Description"
                name="description"
                value={newRequest.description}
                onChange={handleInputChange}
                margin="normal"
                required
                multiline
                rows={4}
                placeholder="Please describe your request in detail..."
                helperText="Please provide specific details about your request to help us process it efficiently."
              />
              
              <Box sx={{ mt: 3 }}>
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  fullWidth
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : 'Submit Request'}
                </Button>
              </Box>
            </Box>
          </Item>
        </Grid>
        
        <Grid item xs={12} md={7}>
          <Item>
            <Typography variant="h6" component="h2" gutterBottom>
              Your Request History
            </Typography>
            
            {loading && requests.length === 0 ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
                <CircularProgress />
              </Box>
            ) : requests.length > 0 ? (
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Type</TableCell>
                      <TableCell>Date</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {requests.map((request) => (
                      <TableRow key={request.id}>
                        <TableCell>
                          {requestTypes.find(t => t.value === request.type)?.label || request.type}
                        </TableCell>
                        <TableCell>
                          {new Date(request.createdAt).toLocaleDateString()}
                        </TableCell>
                        <TableCell>
                          {renderRequestStatus(request.status)}
                        </TableCell>
                        <TableCell>
                          <Button 
                            size="small" 
                            onClick={() => handleViewDetails(request)}
                          >
                            Details
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            ) : (
              <Box sx={{ p: 2, textAlign: 'center' }}>
                <Typography color="text.secondary">
                  You haven't submitted any GDPR requests yet.
                </Typography>
              </Box>
            )}
          </Item>
        </Grid>
      </Grid>
      
      <Dialog open={dialogOpen} onClose={handleCloseDialog}>
        {selectedRequest && (
          <>
            <DialogTitle>
              {requestTypes.find(t => t.value === selectedRequest.type)?.label || selectedRequest.type}
            </DialogTitle>
            <DialogContent>
              <DialogContentText>
                <Box sx={{ mb: 2 }}>
                  <strong>Request ID:</strong> {selectedRequest.id}
                </Box>
                <Box sx={{ mb: 2 }}>
                  <strong>Description:</strong> {selectedRequest.description}
                </Box>
                <Box sx={{ mb: 2 }}>
                  <strong>Status:</strong> {renderRequestStatus(selectedRequest.status)}
                </Box>
                <Box sx={{ mb: 2 }}>
                  <strong>Submitted:</strong> {new Date(selectedRequest.createdAt).toLocaleString()}
                </Box>
                <Box sx={{ mb: 2 }}>
                  <strong>Last Updated:</strong> {new Date(selectedRequest.updatedAt).toLocaleString()}
                </Box>
                
                {selectedRequest.status === 'completed' && selectedRequest.responseData && (
                  <Box sx={{ mt: 3, p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Response Information
                    </Typography>
                    
                    {selectedRequest.responseData.downloadUrl && (
                      <Button 
                        variant="contained" 
                        color="primary" 
                        size="small" 
                        sx={{ mt: 1 }}
                        href={selectedRequest.responseData.downloadUrl}
                        target="_blank"
                      >
                        Download Data
                      </Button>
                    )}
                    
                    {selectedRequest.responseData.expiresAt && (
                      <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                        Download link expires on: {new Date(selectedRequest.responseData.expiresAt).toLocaleString()}
                      </Typography>
                    )}
                  </Box>
                )}
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseDialog}>Close</Button>
            </DialogActions>
          </>
        )}
      </Dialog>
      
      <Snackbar 
        open={notification.open} 
        autoHideDuration={6000} 
        onClose={handleCloseNotification}
      >
        <Alert 
          onClose={handleCloseNotification} 
          severity={notification.severity} 
          variant="filled"
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default GDPRRequestsPage; 