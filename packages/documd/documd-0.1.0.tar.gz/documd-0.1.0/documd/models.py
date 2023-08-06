from collections import defaultdict
from operator import itemgetter


class MarkownDocumentation:

    def __init__(self):
        self.toc = defaultdict(list)
        self.body = defaultdict(list)

    def add_document_to_section(self, section, title, document):
        self.toc[section].append(title)
        self.body[section].append((title, document))

    def _write_toc(self, f):
        f.write('# Table of contents\n')
        for s_index, section in enumerate(sorted(self.toc.keys())):
            if s_index == 0:
                f.write('\n')
            f.write('\n')
            f.write('## {0}\n'.format(section))
            for t_index, title in enumerate(sorted(self.toc[section])):
                f.write('*[{0}](#{1})\n'.format(title, title.lower().replace(' ', '-')))

    def _write_body(self, f):
        f.write('\n')
        for section in sorted(self.body.keys()):
            for (title, doc) in sorted(self.body[section], key=itemgetter(0)):
                f.write('\n\n')
                f.write('### {0}\n'.format(title))
                f.write(doc)

    def write_to_file(self, f):
        self._write_toc(f=f)
        self._write_body(f=f)
