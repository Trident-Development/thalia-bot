from __future__ import annotations

import os
import sqlite3
import tempfile
from logging import getLogger
from random import choice
from string import ascii_lowercase
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import boto3
from botocore.exceptions import ClientError

from config import AWS_ACCESS_KEY_ID
from config import AWS_SECRET_ACCESS_KEY


_logger = getLogger(__name__)


class S3Model:
    # set by subclass
    table_name: str  # name of the sqlite table
    bucket: str  # s3 bucket name
    filename: str  # name of the db file
    file_object_url: str  # object url for the db file
    aws_region: str  # aws s3 bucket region
    columns: Dict[str, str]  # map each column to its sqlite data type

    def __init__(self) -> None:
        raise NotImplementedError()

    def save(self) -> bool:
        return self.add_record(**self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        return {k: getattr(self, k) for k in self.columns.keys()}

    @classmethod
    def select(cls, **kwargs) -> Optional[List[S3Model]]:
        dbfile = "".join(choice(ascii_lowercase) for _ in range(20))
        if not cls._download_s3_file(dbfile):
            return None

        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()

        try:
            cursor.execute(
                f"SELECT * FROM {cls.table_name}"
                + (
                    f" WHERE {','.join([f'{k}=?' for k  in kwargs.keys()])};"
                    if kwargs
                    else ""
                )
            )
        except sqlite3.Error:
            _logger.error("An error occured while executing query")
            return None

        result = [
            cls(**{k: v for k, v in zip(cls.columns.keys(), record)})
            for record in cursor.fetchall()
        ]
        conn.close()
        os.remove(dbfile)
        return result

    @classmethod
    def add_record(cls, **kwargs) -> bool:
        return cls._write_query(
            f"""
            INSERT INTO {cls.table_name}
            ({','.join(kwargs.keys())})
            VALUES
            ({','.join("?" for _ in kwargs)});
            """,
            tuple(kwargs.values()),
        )

    @classmethod
    def delete_record(cls, **kwargs) -> bool:
        return cls._write_query(
            f"""
            DELETE FROM {cls.table_name}
            WHERE
            {','.join([f'{k}=?' for k  in kwargs.keys()])}
            ;""",
            tuple(kwargs.values()),
        )

    @classmethod
    def init_db(cls) -> str:
        fd, temp_dbfile = tempfile.mkstemp(dir=".")

        conn = sqlite3.connect(temp_dbfile)
        cursor = conn.cursor()

        cursor.execute(
            f"CREATE TABLE {cls.table_name} ("
            + ", ".join(
                f"{colname} {datatype}" for colname, datatype in cls.columns.items()
            )
            + ");"
        )
        conn.commit()
        conn.close()

        ret_val = cls._upload_to_s3(temp_dbfile)

        os.close(fd)
        os.remove(temp_dbfile)
        return ret_val

    @classmethod
    def _write_query(
        cls, query: str, params: Union[Tuple[str], List[Tuple[str]]]
    ) -> bool:
        dbfile = "".join(choice(ascii_lowercase) for _ in range(20))
        if not cls._download_s3_file(dbfile):
            return False

        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()

        try:
            if isinstance(params, list):
                cursor.executemany(query, params)
            else:
                cursor.execute(query, params)
            conn.commit()
        except sqlite3.Error:
            _logger.error("An error occured while executing query")
        finally:
            conn.close()

        ret_val = cls._upload_to_s3(dbfile)
        os.remove(dbfile)
        return ret_val

    @classmethod
    def _download_s3_file(cls, name_after_download: str) -> bool:
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        s3_client = session.client("s3")
        try:
            s3_client.download_file(
                Bucket=cls.bucket, Key=cls.filename, Filename=name_after_download
            )
        except ClientError:
            _logger.error("An error occured while downloading file from s3")
            return False
        return True

    @classmethod
    def _upload_to_s3(cls, file: str):
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        s3_client = session.client("s3")

        try:
            ret_val = True
            s3_client.upload_file(file, cls.bucket, cls.filename)
        except ClientError:
            ret_val = False
            _logger.error("An error occured while uploading file to s3")

        return ret_val

    @staticmethod
    def _get_credentials(_):
        return (
            S3Model.aws_region,
            AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY,
            os.environ.get("AWS_SESSION_TOKEN"),
        )
