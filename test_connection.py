import os
from google.cloud import bigquery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_connection():
    """Test BigQuery connection using service account"""

    # Set credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "./gcp-key.json"
    )
    project_id = os.getenv("GCP_PROJECT_ID", "healthcare-data-project-462311")

    try:
        # Initialize client
        client = bigquery.Client(project=project_id)

        # Simple query
        query = """
            SELECT
                'Connected successfully!' as status,
                CURRENT_TIMESTAMP() as timestamp,
                @@project_id as project
        """

        print(f"🔍 Testing connection to project: {project_id}")
        query_job = client.query(query)
        results = query_job.result()

        for row in results:
            print(f"✅ {row.status}")
            print(f"📅 Timestamp: {row.timestamp}")
            print(f"🏗️  Project: {row.project}")

        return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


if __name__ == "__main__":
    test_connection()

# python test_aws_connection.py