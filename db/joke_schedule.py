from db.s3_model import S3Model


class JokeSchedule(S3Model):
    table_name: str = "joke_schedule"
    bucket: str = "thalia-bot-bucket"
    filename: str = "main-db-file"
    file_object_url: str = (
        "https://thalia-bot-bucket.s3.us-west-1.amazonaws.com/main-db-file"
    )
    aws_region: str = "us-west-1"
    columns = {"channel_id": "INTEGER", "cron_expression": "TEXT"}

    def __init__(self, **kwargs) -> None:
        self.channel_id: int = kwargs["channel_id"]
        self.cron_expression: str = kwargs["cron_expression"]
