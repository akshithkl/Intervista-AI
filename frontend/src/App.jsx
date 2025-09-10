// frontend/src/App.jsx
import React, { useState, useEffect } from 'react';
import { Container, Typography, Grid, Card, CardContent, Box, Tabs, Tab, CircularProgress, Alert, Paper } from '@mui/material';
import { jobAPI, testAPI } from './services/api';
import InterviewPractice from './components/InterviewPractice';
import './App.css';

function App() {
  const [jobRoles, setJobRoles] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [currentTab, setCurrentTab] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const initializeApp = async () => {
      try {
        // Test API connection
        await testAPI();
        
        // Fetch job roles
        const response = await jobAPI.getJobRoles();
        setJobRoles(response.data);
      } catch (error) {
        console.error('Error initializing app:', error);
        setError('Failed to connect to the server. Make sure the Django backend is running on port 8000.');
      } finally {
        setLoading(false);
      }
    };

    initializeApp();
  }, []);

  const handleJobSelect = (job) => {
    setSelectedJob(job);
    setCurrentTab(1); // Switch to interview tab
  };

  if (loading) {
    return (
      <div className="app-container">
        <Container maxWidth={false} sx={{ width: '100%' }}>
          <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh" flexDirection="column">
            <CircularProgress size={60} thickness={4} className="loading-spinner" sx={{ mb: 3 }} />
            <Typography variant="h6" sx={{ color: 'white', fontWeight: 600 }}>
              Loading Intervista...
            </Typography>
          </Box>
        </Container>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-container">
        <Container maxWidth={false} sx={{ width: '100%', px: { xs: 2, sm: 3, md: 4 } }}>
          <Paper className="glass-card" sx={{ p: 4, mt: 4 }}>
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
            <Typography variant="body1" sx={{ color: 'text.secondary' }}>
              Make sure your Django server is running: <code>python manage.py runserver</code>
            </Typography>
          </Paper>
        </Container>
      </div>
    );
  }

  return (
    <div className="app-container">
      <Container maxWidth={false} sx={{ width: '100%', px: { xs: 2, sm: 3, md: 4 } }}>
        <Box sx={{ py: 6 }}>
          <Box sx={{ textAlign: 'center', mb: 6 }}>
            <Typography variant="h2" component="h1" className="hero-title floating-animation" sx={{ mb: 2 }}>
              Intervista 🚀
            </Typography>
            <Typography variant="h5" sx={{ color: 'white', fontWeight: 500, opacity: 0.9 }}>
              AI-Powered Interview & Career Platform
            </Typography>
            <Typography variant="h6" sx={{ color: 'white', opacity: 0.8, mt: 1 }}>
              Ace Your Technical Interviews
            </Typography>
          </Box>

          <Paper className="tab-container">
            <Tabs 
              value={currentTab} 
              onChange={(e, newValue) => setCurrentTab(newValue)} 
              sx={{ 
                '& .MuiTab-root': { 
                  color: 'white', 
                  fontWeight: 600,
                  '&.Mui-selected': { 
                    color: 'white',
                    background: 'rgba(255, 255, 255, 0.1)',
                    borderRadius: '8px'
                  }
                },
                '& .MuiTabs-indicator': {
                  background: 'white'
                }
              }}
              centered
            >
              <Tab label="🎯 Job Roles" />
              <Tab label="💬 Interview Practice" disabled={!selectedJob} />
            </Tabs>
          </Paper>

          {currentTab === 0 && (
            <>
              <Typography variant="h4" sx={{ color: 'white', textAlign: 'center', mb: 4, fontWeight: 600 }}>
                🎯 Choose Your Career Path
              </Typography>
              
              <Grid container spacing={4}>
                {jobRoles.map((job, index) => (
                  <Grid item xs={12} sm={6} md={4} key={job.id}>
                    <Card 
                      className="job-card"
                      sx={{ 
                        height: '180px',
                        background: `linear-gradient(135deg, ${['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'][index % 6]} 0%, ${['#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#667eea'][index % 6]} 100%)`,
                        position: 'relative',
                        overflow: 'hidden'
                      }}
                      onClick={() => handleJobSelect(job)}
                    >
                      <CardContent sx={{ 
                        display: 'flex', 
                        flexDirection: 'column', 
                        justifyContent: 'center', 
                        height: '100%',
                        position: 'relative',
                        zIndex: 2
                      }}>
                        <Typography variant="h5" component="h2" sx={{ fontWeight: 'bold', textAlign: 'center', mb: 1 }}>
                          {job.title}
                        </Typography>
                        <Typography variant="body2" sx={{ opacity: 0.9, textAlign: 'center', fontSize: '0.9rem' }}>
                          {job.description || 'Start your interview preparation journey'}
                        </Typography>
                        <Box sx={{ textAlign: 'center', mt: 2 }}>
                          <Typography variant="caption" sx={{ 
                            background: 'rgba(255, 255, 255, 0.2)', 
                            padding: '4px 12px', 
                            borderRadius: '20px',
                            fontSize: '0.75rem'
                          }}>
                            Click to Start →
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
                
                {jobRoles.length === 0 && (
                  <Grid item xs={12}>
                    <Paper className="glass-card" sx={{ p: 4, textAlign: 'center' }}>
                      <Typography variant="h6" sx={{ mb: 2, color: 'text.primary' }}>
                        🚀 Ready to Get Started?
                      </Typography>
                      <Alert severity="info" sx={{ mb: 2 }}>
                        No job roles found. Add some job roles through the Django admin at{' '}
                        <a href="http://localhost:8000/admin" target="_blank" rel="noopener noreferrer" style={{ color: '#1976d2', fontWeight: 'bold' }}>
                          http://localhost:8000/admin
                        </a>
                      </Alert>
                      <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                        Once you add job roles, you'll be able to start practicing interviews!
                      </Typography>
                    </Paper>
                  </Grid>
                )}
              </Grid>
            </>
          )}

          {currentTab === 1 && selectedJob && (
            <Paper className="glass-card" sx={{ p: 4 }}>
              <InterviewPractice selectedJob={selectedJob} />
            </Paper>
          )}
        </Box>
      </Container>
    </div>
  );
}

export default App;