# providers/s3/engine — S3-compatible engine

from fsf.ui import fail


def run(config, debug=False):
    import boto3
    from botocore.config import Config as BotoConfig
    from botocore.exceptions import ClientError, EndpointConnectionError, NoCredentialsError

    endpoint = config.get("endpoint")
    if endpoint and not endpoint.startswith("http"):
        endpoint = "https://" + endpoint
    access_key_id = config.get("access_key_id")
    secret_access_key = config.get("secret_access_key")
    bucket = config.get("bucket")
    region = config.get("region", "us-east-1")
    prefix = config.get("prefix", "")

    if not all([endpoint, access_key_id, secret_access_key, bucket]):
        raise ValueError("endpoint, access_key_id, secret_access_key, and bucket are required")

    session = boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )

    s3 = session.client(
        "s3",
        endpoint_url=endpoint,
        region_name=region,
        config=BotoConfig(connect_timeout=10, read_timeout=30),
    )

    try:
        result = {}
        paginator = s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

        for page in pages:
            for obj in page.get("Contents", []):
                key = obj["Key"]
                response = s3.get_object(Bucket=bucket, Key=key)
                body = response["Body"].read()
                result[key] = body
        return result
    except NoCredentialsError:
        fail("Authentication failed. Check your Access Key ID and Secret Access Key.")
    except EndpointConnectionError:
        fail(f"Unable to connect to endpoint: {endpoint}")
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "NoSuchBucket":
            fail(f"Bucket not found: {bucket}")
        elif code == "AccessDenied":
            fail("Access denied. Check your credentials and bucket permissions.")
        elif code in ("InvalidAccessKeyId", "SignatureDoesNotMatch"):
            fail("Authentication failed. Check your Access Key ID and Secret Access Key.")
        else:
            fail(f"S3 error: {code} (run with --debug for details)")
