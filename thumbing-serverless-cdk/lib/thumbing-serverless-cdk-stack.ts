import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

import * as s3n from 'aws-cdk-lib/aws-s3-notifications';

import createBucket from './resources/bucket';
import createLambda from './resources/lambda';
import createS3NotificationtoLambda from './resources/s3-notification-lambda';

import * as process from 'process';

export class ThumbingServerlessCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    
    const bucketName: string = process.env.THUMBING_BUCKET_NAME as string;
    const bucket = createBucket(this,bucketName)
    const lambda = createLambda(this,bucketName)
    const lambdaNotification = createS3NotificationtoLambda()


    const lambdaNotification = new s3n.LambdaDestination(lambdaFunction);
    bucket.addEventNotification(s3.EventType.OBJECT_CREATED, new s3n.NotificationKeyFilter({
      prefix: 'raw/',
    }), lambdaNotification);
  }
}
