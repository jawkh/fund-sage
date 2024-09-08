#!/usr/bin/env node

// # Copyright (c) 2024 by Jonathan AW

import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { GtCdtSweStack } from '../lib/gt-cdt-swe-stack';

const app = new cdk.App();
new GtCdtSweStack(app, 'GtCdtSweStack', {
  env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: 'ap-southeast-1' },
});

app.synth();