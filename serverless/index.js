/*
Needed Environment Variables :
TARGET_REGION	us-east-1
BUCKET_NAME	    <name of the bucket where quotes.txt exists>
QUOTES_FILE	    quotes.txt
*/

// Load the SDK for JavaScript
var AWS = require('aws-sdk');
// Set the Region 
AWS.config.update({region: process.env.TARGET_REGION});
var s3 = new AWS.S3();

function randomNumber(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}

exports.handler = (event, context, callback) => {
    // TODO implement
     var params = {
      Bucket: process.env.BUCKET_NAME
     };

     s3.listObjects(params, function(err, data) {
       if (err) {
            console.log(err, err.stack); 
            callback(err,null);
       }
       else {     
            console.log(data); 
            const contents = data["Contents"];
            let quotesFound = false;
            for(let i=0; i < contents.length; i++) {
                if(contents[i]["Key"] === process.env.QUOTES_FILE) {
                    quotesFound = true;
                    break;
                }
            }
            if(quotesFound) {
               s3.getObject({ Bucket: process.env.BUCKET_NAME, Key: process.env.QUOTES_FILE }, function(err2, data2)
                {
                    if(err2) {
                        callback(err2,null);
                    } else {
                        const quotesArr = data2.Body.toString("utf8").split("\r\n");
                        
                       // console.log(quotesArr);
                       callback(null,quotesArr[randomNumber(0, quotesArr.length)]);
                    }
                });
                
            } else {
                callback("Quotes file not found",null);
            }
       }
     });
};
