import os
import urllib.request

import click
import pyarrow.parquet as pq

from limelight.models import Document


def download(url_path, filename):
    click.echo(f"Downloading {url_path} to {filename}")
    with open(filename, "wb") as output:
        with urllib.request.urlopen(url_path) as f:
            output.write(f.read())


if __name__ == "__main__":
    url_path = "https://huggingface.co/datasets/euirim/goodwiki/resolve/main/09_04_2023_v1.parquet?download=true" # noqa
    filename = "var/09_04_2023_v1.parquet"
    if os.path.exists(filename):
        if click.confirm("File already exists. Do you want to overwrite it?"):
            os.remove(filename)
            download(url_path, filename)
    else:
        download(url_path, filename)

    df = pq.read_table(filename).to_pandas()
    total = len(df.index)
    with click.progressbar(
        df.iterrows(), length=total, label=f"Processing {total} documents"
    ) as rows:
        for index, row in rows:
            id = Document(
                id=str(row["pageid"]),
                text=row["markdown"],
                title=row["title"],
                categories=row["categories"],
            ).save()
    click.echo(
        click.style(f"{total} documents from dataset were successfully processed", fg="green")
    )
