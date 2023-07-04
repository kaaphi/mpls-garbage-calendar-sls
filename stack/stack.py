import aws_cdk.aws_lambda
from aws_cdk import (
    Stack,
    aws_s3 as s3, RemovalPolicy,
    aws_s3_deployment as s3_deployment,
)
from constructs import Construct

from calendar_service.calendar_service import CalendarService


class MplsGarbageCalendarStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        website_bucket = s3.Bucket(self, "WebsiteBucket",
                                   public_read_access=True,
                                   block_public_access=s3.BlockPublicAccess.BLOCK_ACLS,
                                   website_index_document="index.html",
                                   removal_policy=RemovalPolicy.DESTROY,
                                   auto_delete_objects=True,
                                   )

        s3_deployment.BucketDeployment(self, "DeployWebsite",
                                       destination_bucket=website_bucket,
                                       sources=[s3_deployment.Source.asset("./static_files")]
                                       )

        CalendarService(self, "CalendarService", website_bucket)


