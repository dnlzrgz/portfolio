# /// script
# requires-python=">=3.12"
# dependencies=[
#   "jinja2>=3.1.6",
#   "markdown>=3.7",
#   "python-frontmatter>=1.1.0",
# ]
# ///

import argparse
import sys
import tomllib
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from random import shuffle
from shutil import copytree, ignore_patterns
from urllib.parse import ParseResult
from urllib.parse import urlparse
import frontmatter
import markdown
from jinja2 import Environment as Jinja2Environment
from jinja2 import FileSystemLoader

# ==============================
# ANSI escape codes for colors
# ==============================

RESET = "\033[0m"
BOLD_RED = "\033[1;31m"
BOLD_GREEN = "\033[1;32m"
BOLD_ORANGE = "\033[1;38;5;214m"

# ==============================
# Custom print functions
# ==============================


def print_error(message: str) -> None:
    print(f"{BOLD_RED}Error{RESET}: {message}")


def print_success(message: str) -> None:
    print(f"{BOLD_GREEN}Ok{RESET}: {message}")


def print_warning(message: str) -> None:
    print(f"{BOLD_ORANGE}Warning{RESET}: {message}")


# ==============================
# Validators
# ==============================


def validate_directory(value: str) -> Path:
    path = Path(value)
    if not path.exists():
        raise Exception(f"Directory '{path}' does not exist.")
    if not path.is_dir():
        raise Exception(f"Path '{path}' is not a directory.")

    return path


def validate_url(url: str) -> ParseResult:
    parsed = urlparse(url)
    if not all([parsed.scheme, parsed.netloc]):
        raise Exception(f"Invalid '{url}'.")

    return parsed


# ==============================
# Configuration
# ==============================


class SiteConfig:
    """
    Represents the required configuration settings for the site.
    """

    def __init__(
        self,
        static_dir: str,
        templates_dir: str,
        content_dir: str,
        build_dir: str,
        base_url: str,
    ) -> None:
        self.static_dir: Path = validate_directory(static_dir)
        self.templates_dir: Path = validate_directory(templates_dir)
        self.content_dir: Path = validate_directory(content_dir)
        self.build_dir: Path = validate_directory(build_dir)
        self.base_url: ParseResult = validate_url(base_url)


class Config:
    """
    Represents the overall configuration for the site.
    """

    def __init__(self, site: SiteConfig, params: dict | None = None) -> None:
        self.site = site
        self.params = params if params is not None else {}


# ==============================
# Util functions
# ==============================


def list_content(path: Path) -> list[str]:
    content_list = [file.relative_to(path).as_posix() for file in path.rglob("*.md")]
    content_list.sort(
        key=lambda x: (x.count("/"), not x.endswith("index.md"), x), reverse=True
    )
    return content_list


def load_config(config_file: Path) -> Config:
    if not config_file or not config_file.exists():
        raise Exception("config file does not exists or was not provided.")

    if not config_file.is_file():
        raise Exception(f"config file '{config_file.name}' is not valid.")

    try:
        raw_toml = config_file.read_text()
        parsed_toml = tomllib.loads(raw_toml)

        site_config = SiteConfig(**parsed_toml["site"])
        params = parsed_toml.get("params", {})

        return Config(site=site_config, params=params)
    except tomllib.TOMLDecodeError as e:
        raise Exception(f"Failed to parse TOML from '{config_file.name}': {e}.")
    except Exception as e:
        raise Exception(f"Error reading '{config_file.name}': {e}")


def copy_static_files(content_path: Path, static_dir: Path, output_path: Path) -> None:
    copytree(
        content_path,
        output_path,
        ignore=ignore_patterns("*.md", "*.xml"),
        dirs_exist_ok=True,
    )
    print_success(f"Cloned non-Markdown files to '{output_path.name}' build folder.")

    copytree(
        static_dir,
        output_path.joinpath(static_dir.name),
        dirs_exist_ok=True,
    )
    print_success(
        f"Cloned static folder '{static_dir.name}' into '{output_path.name}' build folder."
    )


def render_template(template, parent, context, pages):
    if parent == "root":
        return template.render(**context, pages=pages)

    return template.render(**context, pages=pages[parent])


# ==============================
# Jinja2 Filters
# ==============================


def shuffle_list(items: list) -> list:
    shuffle(items)
    return items


# ==============================
# Main function
# ==============================


def build(config: Config) -> None:
    content_path = config.site.content_dir
    static_dir = config.site.static_dir
    templates_dir = config.site.templates_dir
    output_path = config.site.build_dir

    jinja_env = Jinja2Environment(loader=FileSystemLoader(templates_dir))
    jinja_env.globals.update(config=config, now=datetime.now())
    jinja_env.filters["shuffle"] = shuffle_list

    pages = defaultdict(list)

    for page in list_content(content_path):
        relative_path = Path(page)
        absolute_path = content_path / page
        relative_parent_path = relative_path.parent
        parent_name = relative_parent_path.name if relative_parent_path.name else "root"

        source = frontmatter.load(absolute_path)
        content = markdown.markdown(
            source.content, extensions=["fenced_code", "tables", "abbr"]
        )
        template_path = relative_path.with_suffix(".html")

        context = {
            "metadata": source.metadata,
            "content": content,
        }

        page_entry = {
            "url": config.site.base_url.path / relative_path.with_suffix(".html"),
            "metadata": source.metadata,
        }

        try:
            template = jinja_env.get_or_select_template(
                [
                    template_path.as_posix(),
                    (relative_parent_path / "single.html").as_posix(),
                ]
            )
        except Exception as e:
            raise Exception(f"Template not found for '{relative_path}': {e}")

        output = render_template(template, parent_name, context, pages)

        output_file_path = output_path / relative_path.with_suffix(".html")
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        with output_file_path.open("w", encoding="utf-8") as f:
            f.write(output)

        print_success(f"Created '{output_file_path}'.")

        if relative_path.stem == "index":
            rss_template_path = relative_parent_path / "rss.xml"

            try:
                rss_output = jinja_env.get_template(
                    rss_template_path.as_posix()
                ).render(
                    pages=pages[parent_name],
                )
                rss_output_path = output_path / relative_parent_path / "rss.xml"
                with rss_output_path.open("w", encoding="utf-8") as f:
                    f.write(rss_output)

                print_success(f"Created RSS feed for '{relative_parent_path}'.")
            except Exception as e:
                print_warning(
                    f"Skipping RSS feed creation for '{relative_parent_path}': {e}."
                )
        else:
            pages[parent_name].append(page_entry)

    try:
        sitemap_output = jinja_env.get_template("/sitemap.xml").render(pages=pages)
        sitemap_output_path = output_path / "sitemap.xml"
        with sitemap_output_path.open("w", encoding="utf-8") as f:
            f.write(sitemap_output)

        print_success("Created sitemap.xml.")
    except Exception:
        print_warning("Skipping sitemap creation.")
        pass

    copy_static_files(content_path, static_dir, output_path)


def main():
    parser = argparse.ArgumentParser(
        prog="marastatic",
        description="Extremely simple single-file static site generator.",
    )
    parser.add_argument(
        "-c",
        "--config-file",
        type=Path,
        default="config.toml",
        help="Path to the configuration file (TOML).",
    )
    args = parser.parse_args()

    try:
        config = load_config(args.config_file)
        build(config)
    except Exception as e:
        print_error(f"{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
