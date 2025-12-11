'''
Author: haoxingjun
Date: 2025-12-11 23:31:05
Email: haoxingjun@bytedance.com
LastEditors: haoxingjun
LastEditTime: 2025-12-11 23:32:22
Description: file information
Company: ByteDance
'''
import os
import sys
import pyarrow.fs as fs
import lancedb


def _split_db_and_table(uri: str):
    """Split uri like s3://bucket/path/.../table_name into (bucket, db_root_uri, table_name)."""
    if not uri:
        return None, None, None
    scheme = ""
    rest = uri
    if rest.startswith("s3://"):
        scheme = "s3://"
        rest = rest[len("s3://"):]
    elif rest.startswith("tos://"):
        scheme = "tos://"
        rest = rest[len("tos://"):]
    parts = [p for p in rest.split("/") if p]
    if not parts:
        return None, None, None
    bucket = parts[0]
    table_name = parts[-1]
    db_root = "/".join(parts[:-1])
    db_root_uri = f"{scheme}{db_root}" if db_root else None
    return bucket, db_root_uri, table_name


def main():
    # Default to the public demo bucket if env not provided
    uri = os.getenv(
        "LANCEDB_URI",
        "s3://data-analysis-demo-data/lance_catalog/default/imdb_top_1000",
    )
    region = os.getenv("TOS_REGION", "cn-beijing")

    bucket, db_root_uri, table_name = _split_db_and_table(uri)
    if not bucket or not db_root_uri or not table_name:
        print(f"Invalid LANCEDB_URI: {uri}")
        sys.exit(1)

    # Use bucket-scoped TOS S3 endpoint (virtual-hosted style) via LanceDB storage_options
    storage_options = {
        "aws_endpoint": f"https://{bucket}.tos-s3-{region}.volces.com",
        "virtual_hosted_style_request": "true",
        # Do NOT pass any credentials to ensure anonymous access
    }

    print(f"Connecting to LanceDB: root={db_root_uri}, table={table_name}")
    try:
        db = lancedb.connect(db_root_uri, storage_options=storage_options)
        tbl = db.open_table(table_name)
        # Lightweight validation: simply ensure we got a table object
        print("Connection successful. Table type:", type(tbl))
        sys.exit(0)
    except Exception as e:
        print("Open default table failed:", e)
        # Fallback: try metadata table from env or default
        metadata_uri = os.getenv(
            "LANCEDB_METADATA_URI",
            "s3://data-analysis-demo-data/lance_catalog/default/metadata_table",
        )
        m_bucket, m_root, m_table = _split_db_and_table(metadata_uri)
        if not m_bucket or not m_root or not m_table:
            print(f"Invalid LANCEDB_METADATA_URI: {metadata_uri}")
            sys.exit(2)
        m_opts = {
            "aws_endpoint": f"https://{m_bucket}.tos-s3-{region}.volces.com",
            "virtual_hosted_style_request": "true",
        }
        print(f"Trying metadata table: root={m_root}, table={m_table}")
        try:
            mdb = lancedb.connect(m_root, storage_options=m_opts)
            mtbl = mdb.open_table(m_table)
            print(f"Connection successful. Opened metadata table: {m_table}. Type: {type(mtbl)}")
            sys.exit(0)
        except Exception as e2:
            print("Connection failed:", e2)
            sys.exit(2)


if __name__ == "__main__":
    main()
