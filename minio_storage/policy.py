import enum
import json


class Policy(enum.Enum):
    none = "NONE"
    get = "GET_ONLY"
    read = "READ_ONLY"
    write = "WRITE_ONLY"
    read_write = "READ_WRITE"

    def bucket(
        self, bucket_name, json_encode=True, *args
    ):
        policies = {
            Policy.get: _get,
            Policy.read: _read,
            Policy.write: _write,
            Policy.read_write: _read_write,
            Policy.none: _none,
        }
        pol = policies[self](bucket_name)
        if json_encode:
            return json.dumps(pol)
        return pol


def _none(bucket_name):
    return {"Version": "2012-10-17", "Statement": []}


def _get(bucket_name):
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:GetObject"],
                "Resource": ["arn:aws:s3:::{}/*".format(bucket_name)],
            }
        ],
    }


def _read(bucket_name):
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:GetBucketLocation"],
                "Resource": ["arn:aws:s3:::{}".format(bucket_name)],
            },
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:ListBucket"],
                "Resource": ["arn:aws:s3:::{}".format(bucket_name)],
            },
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:GetObject"],
                "Resource": ["arn:aws:s3:::{}/*".format(bucket_name)],
            },
        ],
    }


def _write(bucket_name):
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:GetBucketLocation"],
                "Resource": ["arn:aws:s3:::{}".format(bucket_name)],
            },
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:ListBucketMultipartUploads"],
                "Resource": ["arn:aws:s3:::{}".format(bucket_name)],
            },
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": [
                    "s3:ListMultipartUploadParts",
                    "s3:AbortMultipartUpload",
                    "s3:DeleteObject",
                    "s3:PutObject",
                ],
                "Resource": ["arn:aws:s3:::{}/*".format(bucket_name)],
            },
        ],
    }


def _read_write(bucket_name):
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:GetBucketLocation"],
                "Resource": ["arn:aws:s3:::{}".format(bucket_name)],
            },
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:ListBucket"],
                "Resource": ["arn:aws:s3:::{}".format(bucket_name)],
            },
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:ListBucketMultipartUploads"],
                "Resource": ["arn:aws:s3:::{}".format(bucket_name)],
            },
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": [
                    "s3:AbortMultipartUpload",
                    "s3:DeleteObject",
                    "s3:GetObject",
                    "s3:ListMultipartUploadParts",
                    "s3:PutObject",
                ],
                "Resource": ["arn:aws:s3:::{}/*".format(bucket_name)],
            },
        ],
    }
