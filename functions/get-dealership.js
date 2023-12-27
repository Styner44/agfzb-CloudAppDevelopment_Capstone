const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const Cloudant = require('@cloudant/cloudant');
// Initialize Cloudant connection with IAM authentication
async function dbCloudantConnect() {
    try {
        const cloudant = Cloudant({
            account: '41b72835-e355-48ae-9d54-2ba6dc3c140e-bluemix',
            plugins: { iamauth: { iamApiKey: 'AOk7Ln1k62vPK4QYt_dvblE2NKU_fFNG1wNfV6YJzcU8' } }
        });
        const db = cloudant.use('dealerships');
        console.info('Connect success! Connected to DB');
        return db;
    } catch (err) {
        console.error('Connect failure: ' + err.message + ' for Cloudant DB');
        throw err;
    }
}
let db;
(async () => {
    db = await dbCloudantConnect();
})();
app.use(express.json());
// Define a route to get all dealerships with optional state and ID filters
app.get('/dealerships/get', (req, res) => {
    const { state, id } = req.query;
    // Create a selector object based on query parameters
    const selector = {};
    if (state) {
        selector.state = state;
    }
    
    if (id) {
        selector.id = parseInt(id); // Filter by "id" with a value of 1
    }
    const queryOptions = {
        selector,
        limit: 10, // Limit the number of documents returned to 10
    };
    db.find(queryOptions, (err, body) => {
        if (err) {
            console.error('Error fetching dealerships:', err);
            res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
        } else {
            const dealerships = body.docs;
            res.json(dealerships);
        }
    });
});
app.listen(port, () => {
    console.log();
});
