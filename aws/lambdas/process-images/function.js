import {sharp} from 'sharp';
import * as process from 'process';
import { S3Client, PutObjectCommand, GetObjectCommand } from "@aws-sdk/client-s3";
import * as fs from "fs";

const bucketName = process.env.DEST_BUCKET_NAME
const folderInput = process.env.FOLDER_INPUT
const folderOutput = process.env.FOLDER_OUTPUT

const client = new S3Client();

exports.handler = async (event) => {
  console.log('event',event)

  const srcBucket = event.Records[0].s3.bucket.name;
  const srcKey = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' '));
  console.log('srcBucket',srcBucket)
  console.log('srcKey',srcKey)

  const dstBucket = bucketName;
  const dstKey = srcKey.replace(folderInput,folderOutput)
  console.log('dstBucket',dstBucket)
  console.log('dstKey',dstKey)

  const originalImage = await getOriginalImage(client,srcBucket,srcKey)
  const processedImage = await processImage()
  await uploadProcessedImage()
};

async function getOriginalImage(client,srcBucket,srcKey){
  console.log('get==')
  const params = {
    Bucket: srcBucket,
    Key: srcKey
  };
  console.log('params',params)
  const command = new GetObjectCommand(params);
  const response = await client.send(command);
  const originalImage = fs.createWriteStream("/tmp/png");
  console.log('repsonse',response);
  response.Body.pipe(originalImage)
  return originalImage;
}

async function processImage(image){
  const processedImage = await sharp(image.Body)
    .resize(512, 512)
    .png()
    .toBuffer();
  return processedImage;
}

async function uploadProcessedImage(){
  console.log('upload==')
  const params = {
    Bucket: dstBucket,
    Key: dstKey,
    Body: thumbnail,
    ContentType: 'image/png'
  };
  console.log('params',params)
  const command = new PutObjectCommand(paramsPut);
  const response = await client.send(command);
  console.log('repsonse',response);
}