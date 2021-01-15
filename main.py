import redis
import time

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobClient, ContainerClient


def main():
    host = "localhost"
    port = 6379

    cache = redis.Redis(host, port)

    blob_connection_string = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;" \
                             "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr" \
                             "/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;" \
                             "QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;"

    container_name = "my-files"

    container_client = ContainerClient.from_connection_string(
        blob_connection_string, container_name
    )

    try:
        container_client.delete_container()
    except ResourceNotFoundError:
        pass
    
    container_client.create_container()

    blob_name = "my-file.txt"

    cache.delete(blob_name)

    blob_client = BlobClient.from_connection_string(
        blob_connection_string, container_name, blob_name
    )

    print("Uploading blob...")
    blob_client.upload_blob("Hello!")

    for i in range(4):
        start = time.perf_counter()
        data = cache.get(blob_name)

        if not data:
            print("Cache miss.")
            blob = blob_client.download_blob()
            data = blob.readall()
            cache.set(blob_name, data)
            print(f"File contents: {data}")
        else:
            print("Cache hit.")
            print(f"File contents: {data}")

        print(f"Iteration {i + 1} time: {time.perf_counter() - start:0.4f}s")


if __name__ == "__main__":
    main()
