from collections import defaultdict
import os
import textwrap
from .models import MarkownDocumentation

documents = defaultdict(MarkownDocumentation)


def register(doc_name, section, title):
    def wrapper(resource):
        documents[doc_name].add_document_to_section(
            section=section,
            title=title,
            document=textwrap.dedent(resource.__doc__))
        return resource
    return wrapper


def generate(output_path):
    for doc_name, documentation in documents.items():
        with open(os.path.join(output_path, doc_name), 'w') as f:
            documentation.write_to_file(f=f)
