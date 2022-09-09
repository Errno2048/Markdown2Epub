import os
import markdown
from urllib.parse import urlparse
from pathlib import Path
from imghdr import what as image_what

from bs4 import BeautifulSoup
from svglib.svglib import svg2rlg

from .epub import Epub, _file_escape

def _is_image(file):
    return image_what(file) is not None

def _force_make_parent(file):
    if isinstance(file, Path):
        parent = file.parent
    else:
        parent = os.path.dirname(file)
    os.makedirs(parent, exist_ok=True)

def _isUrl(url):
    _parse = urlparse(url)
    return len(_parse.scheme) > 1 and _parse.scheme.lower() != 'file'

_md_extensions = [
    'abbr', 'attr_list', 'def_list',
    'fenced_code', 'footnotes', 'md_in_html', 'tables',
]

def _md2html(md):
    html = markdown.markdown(md, extensions=_md_extensions)
    return html

def _to_etree(src, md=False, convert_svg=False, get_ref=False):
    if md:
        html = _md2html(src)
    else:
        html = src
    et = BeautifulSoup(f'<html><body>{html}</body></html>', features='html.parser')
    as_ = et.find_all('a')
    refs = set()
    for a in as_:
        href = a.attrs.get('href', None)
        if href and not _isUrl(href):
            if not os.path.isabs(href):
                info = urlparse(href)
                if info.fragment:
                    refs.add((info.path, info.fragment))
                else:
                    refs.add((info.path, None))
                filename = os.path.basename(info.path)
                if filename.endswith('.md'):
                    # markdown file
                    path = info.path[:-3] + '.html'
                    query = '' if not info.query else f'?{info.query}'
                    fragment = '' if not info.fragment else f'#{info.fragment}'
                    a.attrs['href'] = f'{path}{query}{fragment}'
    if convert_svg:
        imgs = et.find_all('img')
        for img in imgs:
            src_ = img.attrs.get('src', None)
            if src_ and not _isUrl(src_):
                if not os.path.isabs(src_):
                    if src_.endswith('.svg'):
                        src_ = src_[:-4] + '.png'
                        img.attrs['src'] = src_
    if get_ref:
        return et, refs
    return et

def _etree_to_string(et : BeautifulSoup):
    res = []
    for _item in et.find_all('head'):
        for item in _item.children:
            res.append(str(item))
    for _item in et.find_all('body'):
        for item in _item.children:
            res.append(str(item))
    res = ''.join(res)
    return res

def _folder2epub(epub : Epub, src, css=None, convert_svg=False, encoding='utf8'):
    path = Path(src)

    # cover
    cover = None
    for _file in os.listdir(path):
        file = path / _file
        if os.path.isfile(file):
            if file.name.lower() == 'readme.md':
                #cover = Path() / (_file[:-3] + '.html')
                cover = Path() / _file
                break
            elif file.name.lower() == 'index.htm' or file.name.lower() == 'index.html':
                cover = Path() / _file
                break

    # traverse and convert
    _filtered = (Path('.git'), )

    file_list = []
    _file_stack = [Path()]
    while _file_stack:
        _path = _file_stack.pop()
        files = reversed(os.listdir(path / _path))
        _files = []
        for file in files:
            new_path = _path / file
            if os.path.isfile(path / new_path):
                if new_path != cover:
                    _files.append(new_path)
            else:
                if not new_path in _filtered:
                    _file_stack.append(new_path)
        file_list.extend(reversed(_files))

    if cover:
        if cover.name.endswith('.md'):
            dst_file = cover.parent / (cover.name[:-3] + '.html')
            with open(path / cover, 'r', encoding=encoding) as f:
                content = f.read()
            et = _to_etree(content, md=True, convert_svg=convert_svg)
            et_str = _etree_to_string(et)
            title = cover.name[:-3]
            page = epub.add_cover_page(str(dst_file), title, et_str, file=str(dst_file))
            if css:
                page.css.append(css)
        else:
            dst_file = cover
            with open(path / cover, 'r', encoding=encoding) as f:
                content = f.read()
            et = _to_etree(content, md=False, convert_svg=convert_svg)
            et_str = _etree_to_string(et)
            dot_pos = cover.name.rfind('.')
            if dot_pos >= 0:
                title = cover.name[:dot_pos]
            else:
                title = cover.name
            page = epub.add_cover_page(str(dst_file), title, et_str, file=str(dst_file))

    temp_files = []
    for file in file_list:
        if file.name.endswith('.md'):
            # markdown file
            dst_file = file.parent / (file.name[:-3] + '.html')
            with open(path / file, 'r', encoding=encoding) as f:
                content = f.read()
            et = _to_etree(content, md=True, convert_svg=convert_svg)
            et_str = _etree_to_string(et)
            page = epub.add_page(str(dst_file), file.name[:-3], et_str, file=str(dst_file))
            if css:
                page.css.append(css)
        elif file.name.endswith('.html') or file.name.endswith('.htm'):
            # html file
            dst_file = file
            with open(path / file, 'r', encoding=encoding) as f:
                content = f.read()
            et = _to_etree(content, md=False, convert_svg=convert_svg)
            et_str = _etree_to_string(et)
            dot_pos = file.name.rfind('.')
            if dot_pos >= 0:
                title = file.name[:dot_pos]
            else:
                title = file.name
            page = epub.add_page(str(dst_file), title, et_str, file=str(dst_file))
        elif convert_svg and file.name.endswith('.svg'):
            # svg file
            rlg = svg2rlg(path / file)
            _temp_file = file.name
            image_file = file.parent / (_temp_file + '.png')
            temp_files.append(path / image_file)
            rlg.save(['png'], fnRoot=_temp_file, outDir=path / file.parent)
            epub.add_image(_file_escape(image_file), str(path / image_file), str(image_file))
        elif _is_image(path / file):
            epub.add_image(_file_escape(str(file)), str(path / file), str(file))
        else:
            # other files
            epub.add_others(str(path / file), file, is_path=True)
    return epub, temp_files

def folder2epub(src, *, title=None, author=None, date=None, encoding='utf8', convert_svg=True, css=None, return_temp_files=False):
    epub = Epub(title, author, date)
    epub, temp_files = _folder2epub(epub, src, css=css, convert_svg=convert_svg, encoding=encoding)
    if return_temp_files:
        return epub, temp_files
    return epub
