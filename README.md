# Redis Caching Sample

This Python sample demonstrates caching with Redis using the cache-aside pattern. The program asks the cache for a file. 
If the file is not in cache, it is downloaded from Azure blob storage and cached in Redis. 
Subsequent requests return the file from Redis instead of Azure blob storage, resulting in reduced response times.

## Running the Sample

### Start the Containers
The sample contains an ```azure-deploy.yml``` file that starts a Redis and Azurite container. Run ```docker-compose up```
to start the containers.

### Run the Python Program
Run ```python main.py```.  The output should look like the following:

```bash
Uploading blob...
Cache miss.
File contents: b'Hello!'
Iteration 1 time: 0.0120s
Cache hit.
File contents: b'Hello!'
Iteration 2 time: 0.0008s
Cache hit.
File contents: b'Hello!'
Iteration 3 time: 0.0008s
Cache hit.
File contents: b'Hello!'
Iteration 4 time: 0.0008s
```
In the output above, the first request results in a cache miss, which causes the program to download the blob from
Azure. The file is then cached in Redis. Subsequent requests result in cache hits. 
Notice the dramatic reduction in response time. Reading from blob storage is 15 times slower than reading from cache!