const express = require('express');
const Cloudant = require('@cloudant/cloudant');

const app = express();
const port = process.env.PORT || 3000;

// Retrieve the API key and URL from environment variables
const cloudantApiKey = process.env.IBM_CLOUDANT_API_KEY;
const cloudantUrl = process.env.IBM_CLOUDANT_URL;

const cloudant = Cloudant({
    plugins: { iamauth: { iamApiKey: 'AOk7Ln1k62vPK4QYt_dvblE2NKU_fFNG1wNfV6YJzcU8' } },
    url: 'https://41b72835-e355-48ae-9d54-2ba6dc3c140e-bluemix.cloudantnosqldb.appdomain.cloud',
});

function dbCloudantConnect() {
    try {
        const db = cloudant.use('dealerships');
        console.info('Connect success! Connected to DB');
        return db;
    } catch (err) {
        console.error('Connect failure: ' + err.message + ' for Cloudant DB');
        throw err;
    }
}

let db = dbCloudantConnect();

app.use(express.json());

app.get('/dealerships/get', async (req, res) => {
    const { state, id } = req.query;
    const selector = {};
    if (state) {
        selector.state = state;
    }
    if (id) {
        selector.id = parseInt(id);
    }
    const queryOptions = {
        selector,
        limit: 10,
    };
    try {
        const response = await db.find(queryOptions);
        const dealerships = response.docs;
        res.json(dealerships);
    } catch (err) {
        console.error('Error fetching dealerships:', err);
        res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

module.exports = app;
