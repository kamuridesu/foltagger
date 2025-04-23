import asyncio
import sys
from pathlib import Path

from aiohttp.client_exceptions import ClientResponseError

from src.foltagger.folder import load_json
from src.foltagger.state import get_state_tags, save_state
from src.foltagger.tagger import is_tagger_alive, tagger

TASKS: set[asyncio.Task] = set()
SEM = asyncio.Semaphore(20)


async def fetch_server_response(image: bytes):
    for i in range(5):
        try:
            return await tagger(image)
        except ClientResponseError:
            print(f"Failed to load image, retrying {i+1}/5")
            await asyncio.sleep(5)
    return None


async def start(image: Path, tags: list[str]):
    base_path = image.parent.absolute()
    async with SEM:
        print(f"Cheking image {str(image)}", flush=True)
        remote_tags = get_state_tags(str(image.absolute()))
        if remote_tags is None:
            remote_tags = await fetch_server_response(image.read_bytes())
        if remote_tags is None:
            print(f"Could not fetch tags for image {str(image.name)}")
            return
        save_state(str(image.absolute()), remote_tags)
        print(f"Returned tags for {str(image)}: {remote_tags}", flush=True)
        if not tags:
            return
        for tag in tags:
            tag = tag.lower()
            for otag in remote_tags:
                otag = otag.lower()
                if tag in otag:
                    print(f"Found compatible tags to {str(image)}: {tag}")
                    (base_path / tag).mkdir(exist_ok=True)
                    try:
                        (image.absolute()).replace(base_path / tag / image.name)
                    except FileNotFoundError as e:
                        print(f"Could not move {image.absolute()}, err is {e}")


async def main():
    sname = sys.argv[0]
    if len(sys.argv) < 2:
        print(f"Usage: {sname} folder_to_check")
        sys.exit(1)
    folder = Path(sys.argv[1])
    if not Path(folder).exists():
        print("Folder does not exists")
        sys.exit(1)
    tags = load_json("tags.json")
    if not await is_tagger_alive():
        print("Tagger is not available, check the URL and try again")
        sys.exit(1)
    for image in folder.glob("*"):
        if image.is_dir():
            continue
        task = asyncio.get_event_loop().create_task(start(image, tags))
        TASKS.add(task)
        task.add_done_callback(lambda t: TASKS.remove(t))
    await asyncio.gather(*TASKS)
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
