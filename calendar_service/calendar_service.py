import aws_cdk
from constructs import Construct
from aws_cdk import (aws_apigateway as apigateway,
                     aws_s3 as s3,
                     aws_lambda_python_alpha as lambda_python,
                     aws_apigatewayv2_alpha as apigateway,
                     aws_apigatewayv2_integrations_alpha as apigateway_integrations)


class CalendarService(Construct):
    def __init__(self, scope: Construct, id: str, website_bucket: s3.IBucket):
        super().__init__(scope, id)

        api_function = lambda_python.PythonFunction(self, "GenerateCalendarHandler",
                                                    entry="./lambda/",
                                                    index="handler.py",
                                                    runtime=aws_cdk.aws_lambda.Runtime.PYTHON_3_9,
                                                    bundling=lambda_python.BundlingOptions(
                                                        asset_excludes=["tests"]
                                                    ),
                                                    environment={
                                                        "bucket_name": website_bucket.bucket_name
                                                    }
                                                    )

        website_bucket.grant_read_write(api_function)

        calendar_handler_integration = apigateway_integrations.HttpLambdaIntegration("CalendarIntegration",
                                                                                     handler=api_function
                                                                                     )

        http_api = apigateway.HttpApi(self, "GenerateCalendarApi")

        http_api.add_routes(
            path="/update/{schedule_day}",
            methods=[apigateway.HttpMethod.PUT],
            integration=calendar_handler_integration
        )
