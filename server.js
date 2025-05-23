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
  // This would typically fetch from a database
  // For now, we'll return sample quotes
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
    }
  ];
  
  res.json(recentQuotes);
});

// Subscription endpoint
app.post('/api/subscribe', (req, res) => {
  const { email, phone } = req.body;
  
  // This would typically save to a database
  console.log(`New subscription: Email=${email}, Phone=${phone || 'not provided'}`);
  
  res.json({ success: true, message: "Subscription successful!" });
});

// Simple health check endpoint
app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

// Catch-all route to return the main index.html for all other routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend', 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Web interface available at: http://localhost:${PORT}`);
});