require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const path = require('path');

const app = express();

// Environment Variables
const PORT = process.env.PORT || 5000;
const FQDN = process.env.APP_FQDN || 'localhost';
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/collection_db';

// Dynamic CORS Configuration
const allowedOrigins = [
  process.env.FRONTEND_URL,
  `http://${FQDN}`,
  `https://${FQDN}`,
  'http://localhost:3000',
  'http://127.0.0.1:5000'
];

app.use(cors({
  origin: function (origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('CORS policy violation for this FQDN'));
    }
  },
  credentials: true
}));

app.use(express.json());

// Serve Static Files from the "static" folder
app.use('/static', express.static(path.join(__dirname, 'static')));

// Database Connection
mongoose.connect(MONGO_URI)
  .then(() => console.log('MongoDB Connected Successfully'))
  .catch(err => console.error('MongoDB Connection Error:', err));

// MongoDB Schema & Model
const CollectionSchema = new mongoose.Schema({
  name: { type: String, required: true },
  amount: { type: Number, required: true },
  date: { type: Date, default: Date.now }
});

const Collection = mongoose.model('Collection', CollectionSchema);

// API Endpoints
app.post('/api/add', async (req, res) => {
  try {
    const { name, amount } = req.body;
    const newEntry = new Collection({ name, amount });
    await newEntry.save();
    res.status(201).json({ message: "Entry saved successfully!", data: newEntry });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/all', async (req, res) => {
  try {
    const data = await Collection.find();
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Start Server
app.listen(PORT, () => {
  console.log(`Server running on: http://${FQDN}:${PORT}`);
  console.log(`Static assets accessible at: http://${FQDN}:${PORT}/static/logo.png`);
});
