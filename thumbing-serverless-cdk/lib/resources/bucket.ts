import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';

/*
Create a bucket that will contain images we need to process.
 We'll have the following S3 bucket structure:
- avatars
  - original
  - thumb
*/
export default function createBucket(stack: cdk.Stack, bucketName: string): s3.IBucket {
  const bucket = new s3.Bucket(stack, 'ThumbingBucket', {
    bucketName: bucketName,
    removalPolicy: cdk.RemovalPolicy.DESTROY,
  });
  return bucket;
}