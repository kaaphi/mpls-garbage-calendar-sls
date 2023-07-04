import os

import aws_cdk as cdk
from stack.stack import MplsGarbageCalendarStack

app = cdk.App()
MplsGarbageCalendarStack(app, "MplsGarbageCalendarStack",
                         env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                             region=os.getenv('CDK_DEFAULT_REGION')),)

app.synth()
