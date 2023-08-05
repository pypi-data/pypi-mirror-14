
import re
import os
from glob import glob

import click
from PIL import Image, ImageFilter

from . import blog
from .helpers import find_files


IMAGE_MAX_SIZE = 1900
IMAGE_SAVE_OPTIONS = {
    'quality': 100,
    'optimize': True,
    'progressive': True,
}
IMAGES_PATH = 'images'


@blog.command()
@click.argument('path')
@click.pass_context
def photos(context, path):
    """Adds images to the last article"""

    config = context.obj

    article_filename = find_last_article(config['CONTENT_DIR'])
    if not article_filename:
        return click.echo('No articles.')

    images = list(find_images(path))
    if not images:
        return click.echo('Found no images.')

    for filename in images:
        click.secho(filename, fg='yellow')

    if not click.confirm('\nAdd these images to your last article'):
        click.echo('Aborted!')
        context.exit(1)

    url_prefix = os.path.join('{filename}', IMAGES_PATH)
    images_dir = os.path.join(config['CONTENT_DIR'], IMAGES_PATH)
    os.makedirs(images_dir, exist_ok=True)

    urls = []
    for filename in images:
        image_basename = os.path.basename(filename).lower()
        urls.append(os.path.join(url_prefix, image_basename))
        image_filename = os.path.join(images_dir, image_basename)

        if os.path.isfile(image_filename):
            click.echo('Already exists, skipping: {}'.format(image_filename))
        else:
            image = Image.open(filename)
            image.thumbnail((IMAGE_MAX_SIZE, IMAGE_MAX_SIZE))
            image.filter(ImageFilter.SHARPEN)
            click.echo('Saving: {}'.format(image_filename))
            image.save(image_filename, image.format, **IMAGE_SAVE_OPTIONS)

    content = '\n'
    for url in urls:
        content += '\n![image description]({})\n'.format(url)

    click.echo('Adding to article: {}'.format(article_filename))
    with click.open_file(article_filename, 'a') as f:
        f.write(content)
    click.launch(article_filename)


def find_last_article(content_dir):
    articles = list(sorted(glob(os.path.join(content_dir, '*.md'))))
    if not articles:
        return None

    filename = articles[-1]
    date = os.path.basename(filename)[0:10]

    candidates = []
    for filename in articles:
        if os.path.basename(filename)[0:10] == date:
            candidates.append(filename)

    if len(candidates) == 1:
        return candidates[0]

    to_sort = []
    for filename in candidates:
        with click.open_file(filename) as f:
            match = re.search(r'Date: (.+)', f.read())
        creation_date = match.group(1)
        to_sort.append((creation_date, filename))

    return list(sorted(to_sort))[-1][1]


def find_images(path):
    for filename in find_files(path):
        try:
            Image.open(filename)
        except IOError:
            continue
        else:
            yield filename
