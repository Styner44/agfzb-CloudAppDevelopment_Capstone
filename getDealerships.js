const Cloudant = require('@cloudant/cloudant');

async function main(params) {
    const cloudant = Cloudant({
        url: params.CLOUDANT_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } },
    });

    const db = cloudant.use('dealerships');
    const response = await db.list({ include_docs: true });

    return { body: response.rows.map(row => row.doc) };
}

exports.main = main;