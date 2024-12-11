def what_does_the_fox_say(batch_df=None, batch_id=None):

    if batch_df is not None:
        print(f"Processing batch {batch_id}")
        print(f"Batch count: {batch_df.count()}")  

    return "Ring-ding-ding-ding-dingeringeding!"
