#!/bin/bash
unset STACK_NAME

while getopts :s: opt; do
  case $opt in
    s)
      STACK_NAME="$OPTARG"
      ;;
    \?) 
      echo "Invalid option -$OPTARG" >&2
      ;;
  esac
done

if [[ -z $STACK_NAME ]]; then
    echo "-s [stack name] not specified"
    exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Deploying stack $STACK_NAME"
aws cloudformation deploy --template-file $DIR/templates/dashboard.yaml --stack-name $STACK_NAME --capabilities CAPABILITY_IAM
BKT=$(aws cloudformation describe-stacks --stack-name $STACK_NAME | jq -r '.Stacks[].Outputs[] | select(.OutputKey == "StaticWebBucket") | .OutputValue')

echo "Uploading webapp to $BKT"
aws s3 cp --recursive ./metrics/website $BKT