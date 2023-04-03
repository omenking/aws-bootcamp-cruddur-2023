import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as path from 'path';

export default function createLambda(stack: cdk.Stack, bucketName: string): lambda.IFunction {
  const code = lambda.Code.fromAsset(path.join(__dirname, '..', '..', '..', 'aws', 'lambdas','process-images'))

  const lambdaFunction = new lambda.Function(stack, 'ThumbLambda', {
    runtime: lambda.Runtime.NODEJS_18_X,
    handler: 'index.handler',
    code: code,
    environment: {
      BUCKET_NAME: bucketName,
    },
  });
  return lambdaFunction
}