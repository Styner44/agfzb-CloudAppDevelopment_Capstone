const express = require('express');
const { CloudantV1, IamAuthenticator } = require('@ibm-cloud/cloudant');
require('dotenv').config();

const app = express();
const port = 3000;

// Initialize Cloudant with settings from your IBM Cloud account
const cloudant = CloudantV1.newInstance({ 
  authenticator: new IamAuthenticator({ 
    apikey: process.env.IAM_API_KEY 
  }), 
  serviceUrl: process.env.COUCH_URL 
});

// Use the 'dealerships' database
const db = 'dealerships';

app.get('/api/dealership', async (req, res) => {
    try {
        const state = req.query.state;
        const response = await cloudant.postAllDocs({
            db,
            includeDocs: true
        });
        let dealerships = response.result.rows.map(row => row.doc);
        if (state) {
            dealerships = dealerships.filter(dealer => dealer.st === state);
        }
        res.json(dealerships);
    } catch (err) {
        res.status(500).json({ error: 'Something went wrong' });
    }
});

// Parse JSON bodies
app.use(express.json());

// GET endpoint for reviews
app.get('/api/review', async (req, res) => {
    try {
        const dealershipId = req.query.dealershipId;
        const response = await cloudant.postAllDocs({
            db: 'reviews',
            includeDocs: true
        });
        let reviews = response.result.rows.map(row => row.doc);
        if (dealershipId) {
            reviews = reviews.filter(review => review.dealershipId === dealershipId);
        }
        res.json(reviews);
    } catch (err) {
        res.status(500).json({ error: 'Something went wrong' });
    }
});

// POST endpoint for reviews
app.post('/api/review', async (req, res) => {
    try {
        const review = req.body;
        const response = await cloudant.postDocument({
            db: 'reviews',
            document: review
        });
        res.json(response.result);
    } catch (err) {
        res.status(500).json({ error: 'Something went wrong' });
    }
});

app.listen(port, () => {
  console.log(`Express app listening at http://localhost:${port}`);
});