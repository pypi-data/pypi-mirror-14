import jinja2
import os
from .templates import classpath_template, project_template


class EclipseMetadataFile(object):
    def __init__(self, template, name):
        self.template = template
        self.name = name

    def render(self, project_name):
        return jinja2.Template(self.template).render(project_name=project_name)

    def write(self, project_name, path):
        with open(os.path.join(path, self.name), "w") as f:
            f.write(self.render(project_name))


def write_metadata_files(destination, project_name, force):
    if destination is None:
        destination = project_name

    metadata_files = (
        EclipseMetadataFile(classpath_template, ".classpath"),
        EclipseMetadataFile(project_template, ".project")
    )

    for x in metadata_files:
        if not os.path.exists(os.path.join(destination, x.name)) or force:
            x.write(project_name, destination)
