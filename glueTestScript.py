---
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  GitHubRepo:
    Type: "AWS::CodeCommit::Repository"
    Properties:
      RepositoryName: my-repo
      RepositoryDescription: My CodeCommit repository

  GitHubScript:
    Type: "AWS::S3::Object"
    Properties:
      Bucket: my-bucket
      Key: scripts/my-script.py
      Content: |
        # Add the script contents here

  GlueJobRole:
    Type: "AWS::IAM::Role"
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
        - Action:
          - "sts:AssumeRole"
          Effect: "Allow"
          Principal:
            Service:
            - "glue.amazonaws.com"
          Version: "2012-10-17"
      Policies:
        - PolicyName: "glue-job-s3-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
            - Effect: "Allow"
              Action:
              - "s3:GetObject"
              Resource:
              - !Sub "arn:aws:s3:::my-bucket/scripts/my-script.py"

  GlueJob:
    Type: "AWS::Glue::Job"
    Properties:
      Command:
        Name: "glueetl"
        ScriptLocation: !Sub "s3://my-bucket/scripts/my-script.py"
      Role: !GetAtt GlueJobRole.Arn
      AllocatedCapacity: 2
      Timeout: 2880
