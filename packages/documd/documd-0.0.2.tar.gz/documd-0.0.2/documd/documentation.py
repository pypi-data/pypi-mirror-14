from collections import defaultdict
import textwrap

documents = defaultdict(list)


def register(section):
    def wrapper(resource):
        documents[section].append(textwrap.dedent(resource.__doc__))
        return resource
    return wrapper


def generate(output_file):
    sorted_sections = sorted(documents.keys())

    def write_section(of, section, docs):
        of.write('## {0}\n'.format(section))
        for doc in docs:
            of.write('\n')
            of.write(doc)

    with open(output_file, 'w') as f:
        for index, section in enumerate(sorted_sections):
            if index != 0:
                f.write('\n\n\n')
            write_section(of=f, section=section, docs=documents[section])
