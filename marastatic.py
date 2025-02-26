# /// script
# requires-python=">=3.12"
# dependencies = [
#   "jinja2>=3.1.5",
#   "markdown>=3.7",
#   "python-frontmatter>=1.1.0",
#   "rich>=13.9.4",
#   "typer>=0.15.1",
# ]
# ///

import tomllib
from collections import defaultdict
from pathlib import Path
from shutil import copytree, ignore_patterns
from urllib.parse import ParseResult
from typing import Annotated
from urllib.parse import urlparse
import frontmatter
import markdown
import typer
from jinja2 import Environment as Jinja2Environment
from jinja2 import FileSystemLoader
from rich import print

app = typer.Typer()


# ==============================
# Custom exceptions & errors
# ==============================


class ConfigValidationError(Exception):
    pass


# ==============================
# Validators
# ==============================


def validate_directory(value: str) -> Path:
    path = Path(value)
    if not path.exists():
        raise ConfigValidationError(f"Directory '{path}' does not exist.")
    if not path.is_dir():
        raise ConfigValidationError(f"Path '{path}' is not a directory.")

    return path


def validate_url(url: str) -> ParseResult:
    parsed = urlparse(url)
    if not all([parsed.scheme, parsed.netloc]):
        raise ConfigValidationError(f"Invalid '{url}'.")

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


def handle_error(message: str) -> None:
    print(f"[bold italic red]Error:[/] {message}")
    raise typer.Abort()


def list_site_content(path: Path) -> list[str]:
    content_list = []
    for file in path.rglob("*.md"):
        relative_path = file.relative_to(path).as_posix()
        content_list.append(relative_path)

    content_list.sort(key=lambda x: (x.count("/"), not x.endswith("index.md"), x))
    content_list.reverse()
    return content_list


def load_config(config_file: Path) -> Config:
    if not config_file or not config_file.exists():
        handle_error("config file does not exists or was not provided.")

    if not config_file.is_file():
        handle_error(f"config file '{config_file.name}' is not valid.")

    try:
        raw_toml = config_file.read_text()
        parsed_toml = tomllib.loads(raw_toml)

        site_config = SiteConfig(**parsed_toml["site"])
        params = parsed_toml.get("params", {})

        return Config(site=site_config, params=params)
    except tomllib.TOMLDecodeError as e:
        handle_error(f"Failed to parse TOML from '{config_file.name}': {e}")
    except ConfigValidationError as e:
        handle_error(f"Configuration validation failed: {e}")
    except Exception as e:
        handle_error(f"Unexpected error reading '{config_file.name}': {e}")


# ==============================
# Main function
# ==============================


@app.command()
def build(
    config_file: Annotated[
        Path,
        typer.Option(),
    ],
) -> None:
    config = load_config(config_file)

    content_path = Path(config.site.content_dir)
    static_dir = Path(config.site.static_dir)
    templates_dir = Path(config.site.templates_dir)
    output_path = Path(config.site.build_dir)

    jinja_env = Jinja2Environment(loader=FileSystemLoader(templates_dir))
    pages = defaultdict(list)

    for page in list_site_content(content_path):
        relative_path = Path(page)
        absolute_path = content_path / page
        relative_parent_path = relative_path.parent
        parent_name = relative_parent_path.name
        parent_name = parent_name if parent_name else "root"

        source = frontmatter.load(absolute_path)
        content = markdown.markdown(source.content)

        template_name = f"{relative_path.stem}.html"
        template_path = f"{relative_parent_path}/{template_name}"

        context = {
            "site": config.site,
            "params": config.params,
            "metadata": source.metadata,
            "content": content,
        }

        page_entry = {
            "url": f"{config.site.base_url.path}/{relative_path.with_suffix('.html')}",
            "metadata": source.metadata,
        }

        try:
            template = jinja_env.get_or_select_template(
                [
                    template_path,
                    f"{relative_parent_path}/single.html",
                ]
            )
        except Exception as e:
            handle_error(f"Template not found for '{relative_path}': {e}")

        if parent_name == "root":
            output = template.render(
                **context,
                pages=pages,
            )
        else:
            output = template.render(
                **context,
                pages=pages[parent_name],
            )

        pages[parent_name].append(page_entry)

        output_file_path = output_path / relative_path.with_suffix(".html")
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        output_file_path.write_text(output, encoding="utf-8")

        print(f"[bold green]Ok:[/] Created '{output_file_path}'.")

        if relative_path.stem == "index":
            rss_template_path = f"{relative_parent_path}/rss.xml"
            try:
                rss_output = jinja_env.get_template(rss_template_path).render(
                    site=config.site,
                    params=config.params,
                    pages=pages[parent_name],
                )
                rss_output_path = output_path / f"{relative_parent_path}/rss.xml"
                rss_output_path.write_text(rss_output, encoding="utf-8")

                print(
                    f"[bold green]Ok:[/] Created RSS feed for '{relative_parent_path}'."
                )
            except Exception:
                pass

        sitemap_template_path = f"{relative_parent_path}/sitemap.xml"
        try:
            sitemap_output = jinja_env.get_template(sitemap_template_path).render(
                site=config.site,
                params=config.params,
                pages=pages,
            )
            sitemap_output_path = output_path / f"{relative_parent_path}/sitemap.xml"
            sitemap_output_path.write_text(sitemap_output, encoding="utf-8")

            print("[bold green]Ok:[/] Created sitemap.xml.")
        except Exception:
            pass

    copytree(
        content_path,
        output_path,
        ignore=ignore_patterns("*.md", "*.xml}"),
        dirs_exist_ok=True,
    )
    print(
        f"[bold green]Ok:[/] Cloned non-Markdown files to '{output_path.name}' build folder."
    )

    copytree(
        static_dir,
        output_path.joinpath(static_dir.name),
        dirs_exist_ok=True,
    )
    print(
        f"[bold green]Ok:[/] Cloned static folder '{static_dir.name}' into '{output_path.name}' build folder."
    )


def main():
    app()


if __name__ == "__main__":
    main()
