import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';
import * as process from 'process';
import * as path from 'path';

export class ThumbingServerlessCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    
    const bucketName: string = process.env.THUMBING_BUCKET_NAME || 'cruddur-assets';
    const folderInput: string = process.env.S3_FOLDER_INPUT || 'avatars/raw/'
    const folderOutput: string = process.env.S3_FOLDER_OUTPUT || 'avatars/processed/'
    const webhookUrl: string = process.env.WEBHOOK_URL || 'https://api.cruddur.com/webhook/avatar/processed'
    const topicName: string = process.env.TOPIC_NAME || 'cruddur-avatar'
    const functionPath: string = path.join(__dirname, '..', '..', '..', 'aws', 'lambdas','process-images')

    const bucket = this.createBucket(bucketName)
    const lambda = this.createLambda(functionPath,bucketName)

    // This could be redundent since we have s3ReadWritePolicy?
    bucket.grantRead(lambda);
    bucket.grantPut(lambda);

    const snsTopic = this.createSnsTopic(topicName)
    this.createSnsSubscription(snsTopic,webhookUrl)

    // S3 Event Notifications
    this.createS3NotifyToSns(folderOutput,snsTopic,bucket)
    this.createS3NotifyToLambda(folderInput,lambda,bucket)

    const s3ReadWritePolicy = this.createPolicyBucketAccess(bucket.bucketArn)
    const snsPublishPolicy = this.createPolicySnSPublish(snsTopic.topicArn)

    lambda.addToRolePolicy(s3ReadWritePolicy);
    lambda.addToRolePolicy(snsPublishPolicy);
  }

  createBucket(bucketName: string): s3.IBucket {
    const logicalName: string = 'ThumbingBucket';
    const bucket = new s3.Bucket(this, logicalName , {
      bucketName: bucketName,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
    return bucket;
  }

  createLambda(functionPath: string, bucketName: string): lambda.IFunction {
    const logicalName = 'ThumbLambda';
    const code = lambda.Code.fromAsset(functionPath)
    const lambdaFunction = new lambda.Function(this, logicalName, {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: code,
      environment: {
        BUCKET_NAME: bucketName,
      }
    });
    return lambdaFunction;
  }

  createS3NotifyToLambda(prefix: string, lambda: lambda.IFunction, bucket: s3.IBucket): void {
    const destination = new s3n.LambdaDestination(lambda);
      bucket.addEventNotification(s3.EventType.OBJECT_CREATED_PUT,
      destination,
      {prefix: prefix}
    )
  }

  createS3NotifyToSns(prefix: string, snsTopic: sns.ITopic, bucket: s3.IBucket): void {
    const destination = new s3n.SnsDestination(snsTopic)
    bucket.addEventNotification(
      s3.EventType.OBJECT_CREATED_PUT, 
      destination,
      {prefix: prefix}
    );
  }

  createSnsTopic(topicName: string): sns.ITopic{
    const logicalName = "Topic";
    const snsTopic = new sns.Topic(this, logicalName, {
      topicName: topicName
    });
    return snsTopic;
  }

  createSnsSubscription(snsTopic: sns.ITopic, webhookUrl: string): sns.ISubscription {
    const logicalName = 'MySubscription';
    const snsSubscription = new sns.Subscription(this, logicalName, {
      topic: snsTopic,
      protocol: sns.SubscriptionProtocol.HTTP,
      endpoint: webhookUrl
    });
    return snsSubscription;
  }

  createPolicyBucketAccess(bucketArn: string){
    const s3ReadWritePolicy = new iam.PolicyStatement({
      actions: [
        's3:GetObject',
        's3:PutObject',
      ],
      resources: [
        `${bucketArn}/*`,
      ]
    });
    return s3ReadWritePolicy;
  }

  createPolicySnSPublish(topicArn: string){
    const snsPublishPolicy = new iam.PolicyStatement({
      actions: [
        'sns:Publish',
      ],
      resources: [
        topicArn
      ]
    });
    return snsPublishPolicy;
  }
}