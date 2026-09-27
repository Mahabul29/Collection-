const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

// আপনার MongoDB URL এখানে বসান
const MONGO_URI = "YOUR_MONGODB_URL_HERE";

mongoose.connect(MONGO_URI)
  .then(() => console.log('MongoDB Connected Successfully'))
  .catch(err => console.error('MongoDB Connection Error:', err));

// Schema এবং Model
const CollectionSchema = new mongoose.Schema({
  name: String,
  amount: Number,
  date: { type: Date, default: Date.now }
});

const Collection = mongoose.model('Collection', CollectionSchema);

// API Route: তথ্য সেভ করার জন্য
app.post('/api/add', async (req, res) => {
  try {
    const { name, amount } = req.body;
    const newEntry = new Collection({ name, amount });
    await newEntry.save();
    res.status(201).json({ message: "Data saved successfully!", data: newEntry });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// API Route: সব তথ্য দেখার জন্য
app.get('/api/all', async (req, res) => {
  try {
    const data = await Collection.find();
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(5000, () => {
  console.log('Server is running on port 5000');
});
