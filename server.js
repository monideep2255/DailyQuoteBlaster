const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 5000;

// Middleware to parse JSON bodies
app.use(express.json());

// Serve static files from the frontend directory
app.use(express.static(path.join(__dirname, 'frontend')));

// API endpoint to get recent quotes
app.get('/api/quotes/recent', (req, res) => {
  // Return sample quotes
  const recentQuotes = [
    {
      text: "The best way to predict the future is to create it.",
      author: "Abraham Lincoln",
      date: "2025-05-23",
      category: "motivational"
    },
    {
      text: "Whatever anybody says or does, assume positive intent.",
      author: "Indra Nooyi",
      date: "2025-05-22",
      category: "wisdom"
    },
    {
      text: "Choose your suffering before suffering chooses you!",
      author: "Monideep",
      date: "2025-05-21",
      category: "growth"
    },
    {
      text: "The right decision is always harder in the short term but better in the long term.",
      author: "Dave Ramsey", 
      date: "2025-05-20",
      category: "decisions"
    },
    {
      text: "If you will live like no one else, later you can live like no one else.",
      author: "Dave Ramsey",
      date: "2025-05-19",
      category: "success"
    }
  ];
  
  res.json(recentQuotes);
});

// Subscription endpoint
app.post('/api/subscribe', (req, res) => {
  const { email, phone } = req.body;
  
  // Log the subscription
  console.log(`New subscription: Email=${email || 'not provided'}, Phone=${phone || 'not provided'}`);
  
  // Return success
  res.json({ success: true, message: "Subscription successful!" });
});

// Categories endpoint
app.get('/api/categories', (req, res) => {
  const categories = [
    'motivational',
    'wisdom',
    'growth',
    'decisions',
    'success',
    'general'
  ];
  
  res.json({ categories });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

// Root route
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend', 'index.html'));
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Web interface available at: http://localhost:${PORT}`);
});