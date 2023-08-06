# I'm disgusting. I know.

classpath_template = """<classpath>
  <classpathentry kind="src" path="src"/>
  <classpathentry kind="var" path="wpilib" sourcepath="wpilib.sources"/>
  <classpathentry kind="var" path="networktables" sourcepath="networktables.sources"/>
  <classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.6"/>
  <classpathentry kind="output" path="bin"/>
</classpath>
"""


project_template = """<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
    <name>{{ project_name }}</name>
    <comment></comment>
    <projects>
    </projects>
    <buildSpec>
        <buildCommand>
            <name>org.eclipse.jdt.core.javabuilder</name>
            <arguments>
            </arguments>
        </buildCommand>
    </buildSpec>
    <natures>
        <nature>org.eclipse.jdt.core.javanature</nature>
        <nature>edu.wpi.first.wpilib.plugins.core.nature.FRCProjectNature</nature>
    </natures>
</projectDescription>
"""