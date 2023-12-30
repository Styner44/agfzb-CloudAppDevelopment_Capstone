const express = require('express');
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const app = express();
const port = process.env.PORT || 3000;

// Cloudant credentials and URLs
const cloudantApiKey = 'AOk7Ln1k62vPK4QYt_dvblE2NKU_fFNG1wNfV6YJzcU8';
const cloudantUrl = 'https://41b72835-e355-48ae-9d54-2ba6dc3c140e-bluemix.cloudantnosqldb.appdomain.cloud';

// Initialize Cloudant connection with IAM authentication
async function dbCloudantConnect() {
    try {
        const cloudant = CloudantV1.newInstance({
            iamApiKey: cloudantApiKey,
            url: cloudantUrl
        });
        const db = await cloudant.use('dealerships');
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
app.get('/dealerships/get', async (req, res) => {
    const { state, id } = req.query;
    // Create a selector object based on query parameters
    const selector = {};
    if (state) {
        selector.state = state;
    }
    if (id) {
        selector.id = parseInt(id);
    }
    const queryOptions = {
        selector,
        limit: 10, // Limit the number of documents returned to 10
    };
    try {
        const response = await db.find(queryOptions);
        const dealerships = response.result.docs;
        res.json(dealerships);
    } catch (err) {
        console.error('Error fetching dealerships:', err);
        res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
