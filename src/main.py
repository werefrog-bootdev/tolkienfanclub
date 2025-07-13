import logging
import shutil
from pathlib import Path

from textnode import TextNode, TextType


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
)
logger = logging.getLogger(__name__)


def copy_static(src: Path, dest: Path) -> None:
    """
    Recursively copy all files and subdirectories from `src` to `dest`.
    If `dest` exists, delete it first.
    """
    if dest.exists():
        shutil.rmtree(dest)
        logger.info(f"Deleted existing directory: {dest}")
    dest.mkdir(parents=True)
    logger.info(f"Created directory: {dest}")

    for item in src.iterdir():
        dest_item = dest / item.name
        if item.is_dir():
            copy_static(item, dest_item)
        else:
            shutil.copy2(item, dest_item)
            logger.info(f"Copied file: {item} -> {dest_item}")



def main():
    static_dir = Path("static")
    public_dir = Path("public")
    copy_static(static_dir, public_dir)


if __name__ == '__main__':
    main()