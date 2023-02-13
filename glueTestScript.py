AWSTemplateFormatVersion: '2010-09-09'
Parameters:
  GitHubScript:
    Type: String
    Description: Name of the script file stored in the Github repository
  GitHubRepo:
    Type: String
    Description: URL of the Github repository
Resources:
  GlueJob:
    Type: 'AWS::Glue::Job'
    Properties:
      Command:
        Name: 'pythonshell'
        ScriptLocation: !Sub 'https://raw.githubusercontent.com/${GitHubRepo}/master/${GitHubScript}'
      DefaultArguments:
        '--job-bookmark-option': 'job-bookmark-disable'
      Description: 'A Glue Job to pull a script from a Github repository'
      ExecutionProperty:
        MaxConcurrentRuns: 1
      Name: !Ref 'AWS::StackName'
      Role: !GetAtt [GlueServiceRole, Arn]
      Timeout: 2880
      MaxRetries: 0
  GlueServiceRole:
    Type: 'AWS::IAM::Role'
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: 'Allow'
            Principal:
              Service:
                - 'glue.amazonaws.com'
            Action: 'sts:AssumeRole'
      Policies:
        - PolicyName: 'GlueServiceRolePolicy'
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: 'Allow'
                Action:
                  - 'glue:GetJobRuns'
                  - 'glue:BatchGetJobs'
                  - 'glue:StartJobRun'
                Resource: '*'
