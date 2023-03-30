const sharp = require('sharp');
const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const process = require('process');

const bucket_name = process.env.DEST_BUCKET_NAME

exports.handler = async (event) => {
  const srcBucket = event.Records[0].s3.bucket.name;
  const srcKey = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' '));
  const dstBucket = bucket_name;
  const dstKey = `${srcKey.split('.').slice(0, -1).join('.')}-thumbnail.png`;

  // Retrieve the image from S3
  const params = {
    Bucket: srcBucket,
    Key: srcKey
  };
  const image = await s3.getObject(params).promise();

  // Create a thumbnail of the image
  const thumbnail = await sharp(image.Body)
    .resize(512, 512)
    .png()
    .toBuffer();

  // Upload the thumbnail to S3
  const uploadParams = {
    Bucket: dstBucket,
    Key: dstKey,
    Body: thumbnail,
    ContentType: 'image/png'
  };
  await s3.putObject(uploadParams).promise();
};