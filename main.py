import asyncio
import csv

import tinydb

import GPTParser as gp
from decorator import memoize_with_db
from define import *
from sorting_hat import SortingHat

batch_size = 6
max_retries = 3

db = tinydb.TinyDB("/".join([DB_FOLDER, DB_FILENAME]), ensure_ascii=False)


async def main():
    with open("/".join([INPUT_FOLDER, CSV_FILENAME]), "r") as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        message_index = header.index(MESSAGE_COL_NAME)
        user_id_index = header.index(USER_ID_COL_NAME)

        retries_map = {}
        next_batch = []
        batch_num = 0
        while True:
            while len(next_batch) < batch_size:
                try:
                    row = next(reader)
                    user_id = row[user_id_index]
                    next_batch.append((user_id, row))
                except StopIteration:
                    print("No more rows to read")
                    break

            if not next_batch:
                print("Finished!")
                return
            print(f"Batch {batch_num} Started!")
            batch_num += 1

            sorting_tasks = []
            for user_id, row in next_batch:
                raw_messages_string = row[message_index]

                messages = gp.string_to_messages(raw_messages_string)
                message_segments = gp.segment_messages(messages)
                username = message_segments[gp.SEG_BASIC][1].content

                sorting_hat_on_user = SortingHat.put_on(user_id, username)
                sorting_hat_on_user.read_mind(message_segments, db)

                sorting_tasks.append(sorting_hat_on_user.decide())

            result_flags = await asyncio.gather(*sorting_tasks)
            rows_to_retry = [i for i, x in enumerate(result_flags) if not x]
            retry_batch = []
            for index in rows_to_retry:
                # db.remove(tinydb.Query().user_id == next_batch[index][0])
                if next_batch[index][0] not in retries_map:
                    retries_map[next_batch[index][0]] = 0

                retries_map[next_batch[index][0]] += 1
                if retries_map[next_batch[index][0]] > max_retries:
                    print(
                        f"User {next_batch[index][0]} failed to be sorted after {max_retries} retries"
                    )
                    continue

                print(f"User {next_batch[index][0]} failed to be sorted, retrying")
                retry_batch.append(next_batch[index])
            next_batch = retry_batch


if __name__ == "__main__":
    asyncio.run(main())
