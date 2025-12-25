import asyncio
import json
import os
import urllib.error
import urllib.request

from nats.aio.client import Client as NATS  # noqa: E402

NATS_URL = os.getenv('NATS_URL', 'nats://my-nats.default.svc.cluster.local:4222')
NATS_SUBJECT_TODO_ADDED = os.getenv('NATS_ADDED_SUBJECT', 'todos.added')
NATS_SUBJECT_TODO_DONE = os.getenv('NATS_DONE_SUBJECT', 'todos.done')
# inserted at build time
DISCORD_HOOK_URL = os.getenv(
  'DISCORD_HOOK_URL',
  '',
)


def post_to_discord(webhook_url: str, content: str):
  if webhook_url == 'dev://' or not webhook_url:
    print(content)
  else:
    data = json.dumps({'content': content}).encode('utf-8')
    req = urllib.request.Request(
      webhook_url,
      data=data,
      headers={'Content-Type': 'application/json'},
      method='POST',
    )
    try:
      with urllib.request.urlopen(req, timeout=5) as resp:
        resp.read()
    except urllib.error.HTTPError as e:
      print(f'Discord webhook error {e.code}: {e.read()}')
    except Exception as e:
      print(f'Discord webhook exception: {e}')


async def main():
  nc = NATS()
  await nc.connect(NATS_URL)

  loop = asyncio.get_running_loop()

  async def handler(msg):
    subject = msg.subject
    data = msg.data.decode()

    content = f'[{subject}] {data}'

    # Send message to the Discord channel (post_to_discord is blocking)
    await loop.run_in_executor(None, post_to_discord, DISCORD_HOOK_URL, content)

  await nc.subscribe(NATS_SUBJECT_TODO_ADDED, cb=handler)
  await nc.subscribe(NATS_SUBJECT_TODO_DONE, cb=handler)

  try:
    await asyncio.Event().wait()
  finally:
    await nc.close()


asyncio.run(main())
