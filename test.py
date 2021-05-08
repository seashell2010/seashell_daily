# import re
#
# for statement in ("I love Mary",
#                   "Ich liebe Margot",
#                   "Je t'aime Marie",
#                   "Te amo Maria"):
#
#     if m := re.match(r"I love (\w+)", statement):
#         print("He loves", m.group(1))
#
#     elif m := re.match(r"Ich liebe (\w+)", statement):
#         print("Er liebt", m.group(1))
#
#     elif m := re.match(r"Je t'aime (\w+)", statement):
#         print("Il aime", m.group(1))
#
#     else:
#         print()


import asyncio

async def cancel_me():
    print('cancel_me(): before sleep')

    try:
        # Wait for 1 hour
        await asyncio.sleep(3600)
    except asyncio.CancelledError:
        print('cancel_me(): cancel sleep')
        raise
    finally:
        print('cancel_me(): after sleep')

async def main():
    # Create a "cancel_me" Task
    task = asyncio.create_task(cancel_me())

    # Wait for 1 second
    await asyncio.sleep(1)

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("main(): cancel_me is cancelled now")

asyncio.run(main())

