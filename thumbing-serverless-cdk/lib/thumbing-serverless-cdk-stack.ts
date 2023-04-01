import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';

import process;

export class ThumbingServerlessCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const bucket_name = process.env.THUMBBING_BUCKET_NAME;

    const bucket = new s3.Bucket(this, bucket_name, {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
  }
}
