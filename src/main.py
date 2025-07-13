import logging
import shutil
from pathlib import Path

from markdown_extract import markdown_to_html_node
from textnode import TextNode, TextType


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
)
logger = logging.getLogger(__name__)


CONTENT_DIR = Path("content")
STATIC_DIR = Path("static")
PUBLIC_DIR = Path("public")
TEMPLATE_PATH = Path("template.html")


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


def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.strip().startswith("# "):
            return line.strip()[2:].strip()
    raise ValueError("No H1 heading found in markdown")


def generate_page(from_path: Path, template_path: Path, dest_path: Path) -> None:
    logging.info(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_content = from_path.read_text(encoding="utf-8")
    template_content = template_path.read_text(encoding="utf-8")

    html_node = markdown_to_html_node(from_content)
    html_str = html_node.to_html()

    title = extract_title(from_content)

    result = (
        template_content
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html_str)
    )

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(result, encoding="utf-8")
    logging.info(f"Written HTML to {dest_path}")


def main():
    copy_static(STATIC_DIR, PUBLIC_DIR)

    for markdown_path in CONTENT_DIR.rglob("*.md"):
        relative_path = markdown_path.relative_to(CONTENT_DIR)
        output_path = PUBLIC_DIR / relative_path.with_suffix(".html")
        generate_page(markdown_path, TEMPLATE_PATH, output_path)


if __name__ == '__main__':
    main()