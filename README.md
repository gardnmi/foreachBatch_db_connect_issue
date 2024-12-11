# Databricks Connect ForeachBatch Issue Demo

This demo project showcases how `foreachBatch` does not work locally with Databricks Connect when referencing your own project in pip editable mode.

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

## Steps to Reproduce

1. **Clone this repository:**

   ```bash
   git clone https://github.com/gardnmi/foreachBatch_db_connect_issue.git
   cd foreachBatch_db_connect_issue
   ```

2. **Open the repository in VS Code and open the dev container:**
   - Open VS Code.
   - Use the `Remote - Containers` extension to open the repository in a dev container.

3. **Set up the environment by running the following command in the terminal:**

   ```bash
   task setup_environment
   ```

4. **Authenticate with Databricks Connect:**
   - When prompted, enter the Databricks workspace URL to authenticate.

5. **Run the Python script:**

   ```bash
   python src/my_project
   ```

## Expected Output

The script should run and error with the following message

```bash
2024-12-11 23:31:49.752 | INFO     | __main__:get_spark:36 - Running in local environment. Returning DatabricksSession.

2024-12-11 23:31:50.212 | INFO     | __main__:<module>:67 - Testing local function `what_does_the_cow_say`
2024-12-11 23:31:50.212 | INFO     | __main__:<module>:68 - Running `what_does_the_cow_say` outside of stream
2024-12-11 23:31:50.212 | INFO     | __main__:<module>:69 - Moo Moo Moo
2024-12-11 23:31:50.213 | SUCCESS  | __main__:<module>:70 - `what_does_the_cow_say` function completed

2024-12-11 23:31:50.213 | INFO     | __main__:<module>:72 - Running `what_does_the_cow_say` inside of stream
2024-12-11 23:31:55.196 | SUCCESS  | __main__:<module>:76 - `what_does_the_cow_say` stream completed

------------------------

2024-12-11 23:31:55.197 | INFO     | __main__:<module>:80 - Testing imported function `what_does_the_fox_say`
2024-12-11 23:31:55.198 | INFO     | __main__:<module>:81 - Running `what_does_the_fox_say` outside of stream
2024-12-11 23:31:55.198 | INFO     | __main__:<module>:82 - Ring-ding-ding-ding-dingeringeding!
2024-12-11 23:31:55.199 | SUCCESS  | __main__:<module>:83 - `what_does_the_fox_say` function completed

2024-12-11 23:31:55.199 | INFO     | __main__:<module>:85 - Running `what_does_the_fox_say` inside of stream

ModuleNotFoundError: No module named 'my_project'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/databricks/spark/python/pyspark/sql/connect/streaming/worker/foreach_batch_worker.py", line 90, in main
    func = worker.read_command(pickle_ser, infile)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/databricks/spark/python/pyspark/worker_util.py", line 70, in read_command
    command = serializer._read_with_length(file)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/databricks/spark/python/pyspark/serializers.py", line 196, in _read_with_length
    raise SerializationError("Caused by " + traceback.format_exc())
pyspark.serializers.SerializationError: Caused by Traceback (most recent call last):
  File "/databricks/spark/python/pyspark/serializers.py", line 192, in _read_with_length
    return self.loads(obj)
           ^^^^^^^^^^^^^^^
  File "/databricks/spark/python/pyspark/serializers.py", line 572, in loads
    return cloudpickle.loads(obj, encoding=encoding)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'my_project'
```

## What's Happening

The script runs foreachBatch on a stream twice:

1. First Run: It uses the function what_does_the_cow_say, which is defined in the same module as the stream. This function runs successfully.

2. Second Run: It uses the function what_does_the_fox_say, which is defined in a separate module. This function fails with a ModuleNotFoundError.

To verify that both functions are accessible and working, they are also executed outside of the stream. The function defined in the same module (what_does_the_cow_say) runs without issues, while the function defined in the separate module (what_does_the_fox_say) encounters the error when run within the stream.


## Troubleshooting

If you encounter any issues, please ensure that:

- Docker Desktop is running.
- You have the latest version of VS Code and the `Remote - Containers` extension installed.
- Your Databricks workspace URL is correct and you have the necessary permissions.

For further assistance, please refer to the official documentations for [Docker Desktop](https://docs.docker.com/get-docker/) and [VS Code Dev Containers](https://code.visualstudio.com/docs/remote/containers).
