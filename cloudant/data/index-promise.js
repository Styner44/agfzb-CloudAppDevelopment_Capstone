const Cloudant = require('@cloudant/cloudant');

function getDbs(cloudant) {
    return new Promise((resolve, reject) => {
        cloudant.db.list()
            .then(body => {
                resolve({ dbs: body });
            })
            .catch(err => {
                reject({ err: err });
            });
    });
}

function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });
    let dbListPromise = getDbs(cloudant);
    return dbListPromise;
}

// Test the function
main({
    COUCH_URL: "https://41b72835-e355-48ae-9d54-2ba6dc3c140e-bluemix.cloudantnosqldb.appdomain.cloud",
    IAM_API_KEY: "Udq3_mK0zxdnBA4cx2bBE045ZYD2BtzGF5tGT20fFKOh"
}).then(console.log).catch(console.error);