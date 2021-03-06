===================
Code Class Diagrams
===================

Inheritance Diagrams
====================

Basic Classes
-------------

The following scheme shows the class inheritance diagram of the most imporatant classes in RepTate. Most of them are children of the CmdBase class. In the diagram:

   - Empty ellipses represent **core classes**. Their source code can be found in the ``code`` folder and are they provide the basic functionality to work from the command line (CL version).
   
            - Grey filled rounded boxes represent the **gui classes**. Each core class has a gui counterpart. Each gui class is derived from a core class and a PyQt object (either QWidget or QMainWindow).

   - Green filled boxes represent **PyQt5** classes. Many PyQt5 classes are used within the RepTate code. In the diagram, only two of the most important are shown.

   - Arrows represent inheritance. The arrow goes **from the parent class to the child class**.

.. graphviz::

   digraph foo {
      "CmdBase" [href="../developers/CodeCoreCL.html#cmdbase", target="_top"]
      "Application" [href="../developers/CodeCoreCL.html#application", target="_top"]
      "ApplicationManager" [href="../developers/CodeCoreCL.html#applicationmanager", target="_top"]
      "DataSet" [href="../developers/CodeCoreCL.html#dataset", target="_top"]
      "Theory" [href="../developers/CodeCoreCL.html#theory", target="_top"]
      "Tool" [href="../developers/CodeCoreCL.html#tool", target="_top"]
      "CmdBase" -> "Application";
      "CmdBase" -> "ApplicationManager";
      "CmdBase" -> "DataSet";
      "CmdBase" -> "Theory";
      "CmdBase" -> "Tool";
      "QApplicationWindow" [href="../developers/CodeCoreGUI.html#qapplicationwindow", target="_top", shape="box", style="rounded,filled"]
      "QApplicationManager" [href="../developers/CodeCoreGUI.html#qapplicationmanager", target="_top", shape="box", style="rounded,filled"]
      "QDataSet" [href="../developers/CodeCoreGUI.html#qdataset", target="_top", shape="box", style="rounded,filled"]
      "QTheory" [href="../developers/CodeCoreGUI.html#qtheory", target="_top", shape="box", style="rounded,filled"]
      "QTool" [href="../developers/CodeCoreGUI.html#qtool", target="_top", shape="box", style="rounded,filled"]
      "Application" -> "QApplicationWindow";
      "ApplicationManager" -> "QApplicationManager";
      "DataSet" -> "QDataSet";
      "Theory" -> "QTheory";
      "Tool" -> "QTool";
      "QWidget" [shape=box,fillcolor=palegreen,href="https://doc.qt.io/qt-5/qwidget.html", target="_top", style="filled"]
      "QMainWindow" [shape=box,fillcolor=palegreen,href="https://doc.qt.io/qt-5/qmainwindow.html", target="_top", style="filled"]
      "QWidget" -> "QApplicationWindow" [color=green];
      "QWidget" -> "QDataSet" [color=green];
      "QWidget" -> "QTheory" [color=green];
      "QWidget" -> "QTool" [color=green];
      "QMainWindow" -> "QApplicationManager" [color=green];
   }

``CmdBase`` provides the basic functionality to operate on the command line (CL). RepTate was built first as a CL application and this hierarchical class structure is a reminder of that. The Graphic User Interface (GUI) version of the classes are children of the corresponding CL versions and QWidget class from PyQt (except the QApplicationManager, which is derived from QMainWindow).

Applications
------------

When developing a new application, it is important to keep in mind the class hierarchical structure of application classes in RepTate. In the following scheme, an example diagram of the class inheritance a particular application (**LVE**) is shown). In the diagram:

   - All classes represented by an empty ellipse are CL classes. They must provide the basic functionality of the class (everything that the class needs to work during a CL or a batch session of RepTate). 

   - Classes represented by a filled rounded box are gui classes. They must provide all the GUI functionality of the class (buttons, menus, special features, etc). Simple applications will inherit all the needed GUI functionality from **QApplicationWindow**. More advanced apps will need special implementation of advanced features. 

   - Classes represented by red empty boxes are **metaclasses**. Essentially, it is a class with no functionality. Its only purpose is to select which of the two versions of the application (either CL or GUI) is created, depending on the particular context. 

.. graphviz::

   digraph foo {
      "CmdBase" [href="../developers/CodeCoreCL.html#cmdbase", target="_top"]
      "Application" [href="../developers/CodeCoreCL.html#application", target="_top"]
      "QApplicationWindow" [href="../developers/CodeCoreGUI.html#qapplicationwindow", target="_top", shape="box", style="rounded,filled"]
      "ApplicationLVE" [href="../developers/CodeApplications.html#applicationlve", target="_top", shape=box,color=red]
	   "BaseApplicationLVE" [href="../developers/CodeApplications.html#applicationlve", target="_top"]
	   "CLApplicationLVE" [href="../developers/CodeApplications.html#applicationlve", target="_top"]
	   "GUIApplicationLVE" [href="../developers/CodeApplications.html#applicationlve", target="_top", shape="box", style="rounded,filled"]
      "CmdBase" -> "Application";
      "Application" -> "QApplicationWindow";
      "QApplicationWindow" -> "GUIApplicationLVE";
      "Application" -> "CLApplicationLVE";
      "BaseApplicationLVE" -> "GUIApplicationLVE";
      "BaseApplicationLVE" -> "CLApplicationLVE";
      "CmdBase" -> "ApplicationLVE"
      "ApplicationLVE" -> "CLApplicationLVE" [style=dotted, label="CL", color=red, fontcolor=red];
      "ApplicationLVE" -> "GUIApplicationLVE" [style=dotted, label="GUI", color=red, fontcolor=red];
   }

Note for Victor
^^^^^^^^^^^^^^^

I don't feel very comfortable with this hieararchy for the following reasons:

   - ApplicationLVE is a child of CmdBase but uses none of its functionality. Application LVE is just a metaclass that decides which is the right instance to create, depending on the case (CL or GUI).
   - BaseApplicationLVE uses functionality of Application but it is not a children of it. In fact, VSCode and other editors complain that some of the members of BaseApplicationLVE do not exist. 
   
I never understood well how this structure could work, but the fact is that it does and it was a brilliant solution at the time. In fact, I consider this to be one of the biggest pillars upon which we built RepTate. It was fully your solution, so I want to discuss it with you before applying any changes to this.

Following the considerations above, I suggest the following new inheritance relation:

.. graphviz::

   digraph foo {
      "CmdBase" [href="../developers/CodeCoreCL.html#cmdbase", target="_top"]
      "Application" [href="../developers/CodeCoreCL.html#application", target="_top"]
      "QApplicationWindow" [href="../developers/CodeCoreGUI.html#qapplicationwindow", target="_top", shape="box", style="rounded,filled"]
      "ApplicationLVE" [href="../developers/CodeApplications.html#applicationlve", target="_top", shape=box,color=red]
	   "BaseApplicationLVE" [href="../developers/CodeApplications.html#applicationlve", target="_top"]
	   "CLApplicationLVE" [href="../developers/CodeApplications.html#applicationlve", target="_top"]
	   "GUIApplicationLVE" [href="../developers/CodeApplications.html#applicationlve", target="_top", shape="box", style="rounded,filled"]
      "CmdBase" -> "Application";
      "Application" -> "QApplicationWindow";
      "QApplicationWindow" -> "GUIApplicationLVE";
      "Application" -> "BaseApplicationLVE";
      "BaseApplicationLVE" -> "CLApplicationLVE";
      "BaseApplicationLVE" -> "GUIApplicationLVE";
      "ApplicationLVE" -> "CLApplicationLVE" [style=dotted, label="CL", color=red, fontcolor=red];
      "ApplicationLVE" -> "GUIApplicationLVE" [style=dotted, label="GUI", color=red, fontcolor=red];
   }


Now, the dependencies are clear, and all classes that need to use functionality from another are children of it. ApplicationLVE does not need to be the child of any class because it simply does not use any functionality. It is just a Metaclass. I've tried this implementation for one of the Applications and it seems to work. However, before applying this structure to the overall code, I'd like to know what you think about it. In any case, if I ever try to implement this, I'll do it in a separate branch that we will test thoroughly before merging it to the main.


Theories
--------

Example diagram of the class inheritance of one of the Theories

.. graphviz::

   digraph foo {
      "CmdBase" [href="../developers/CodeCoreCL.html#cmdbase", target="_top"]
      "Theory" [href="../developers/CodeCoreCL.html#theory", target="_top"]
      "QTheory" [href="../developers/CodeCoreGUI.html#qtheory", target="_top", shape="box", style="rounded,filled"]
      "TheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic", target="_top", shape=box, color=red]
      "BaseTheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic", target="_top"]
      "CLTheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic", target="_top"]
      "GUITheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic", target="_top", shape="box", style="rounded,filled"]
      "CmdBase" -> "Theory";
      "Theory" -> "QTheory";
      "QTheory" -> "GUITheoryPolynomial";
      "Theory" -> "CLTheoryPolynomial";
      "BaseTheoryPolynomial" -> "GUITheoryPolynomial";
      "BaseTheoryPolynomial" -> "CLTheoryPolynomial";
      "CmdBase" -> "TheoryPolynomial"
      "TheoryPolynomial" -> "CLTheoryPolynomial" [style=dotted, label="CL", color=red, fontcolor=red];
      "TheoryPolynomial" -> "GUITheoryPolynomial" [style=dotted, label="GUI", color=red, fontcolor=red];
   }

Note for Victor regarding theories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using a similar reasoning as with Applications, I suggest the following new structure:

.. graphviz::

   digraph foo {
      "CmdBase" [href="../developers/CodeCoreCL.html#cmdbase", target="_top"]
      "Theory" [href="../developers/CodeCoreCL.html#theory", target="_top"]
      "QTheory" [href="../developers/CodeCoreGUI.html#qtheory", target="_top", shape="box", style="rounded,filled"]
      "TheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic", target="_top", shape=box, color=red]
      "BaseTheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic", target="_top"]
      "CLTheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic", target="_top"]
      "GUITheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic", target="_top", shape="box", style="rounded,filled"]
      "CmdBase" -> "Theory";
      "Theory" -> "QTheory";
      "QTheory" -> "GUITheoryPolynomial";
      "Theory" -> "BaseTheoryPolynomial";
      "BaseTheoryPolynomial" -> "CLTheoryPolynomial";
      "BaseTheoryPolynomial" -> "GUITheoryPolynomial";
      "TheoryPolynomial" -> "CLTheoryPolynomial" [style=dotted, label="CL", color=red, fontcolor=red];
      "TheoryPolynomial" -> "GUITheoryPolynomial" [style=dotted, label="GUI", color=red, fontcolor=red];
   }



Tools
-----

Example diagram of the class inheritance relation for one of the Tools:

.. graphviz::

   digraph foo {
      "CmdBase" [href="../developers/CodeCoreCL.html#cmdbase", target="_top"]
      "Tool" [href="../developers/CodeCoreCL.html#tool", target="_top"]
      "QTool" [href="../developers/CodeCoreGUI.html#qtool", target="_top", shape="box", style="rounded,filled"]
      "ToolBounds" [href="../developers/CodeTools.html#toolbounds", target="_top", shape=box, color=red]
      "BaseToolBounds" [href="../developers/CodeTools.html#toolbounds", target="_top"]
      "CLToolBounds" [href="../developers/CodeTools.html#toolbounds", target="_top"]
      "GUIToolBounds" [href="../developers/CodeTools.html#toolbounds", target="_top", shape="box", style="rounded,filled"]
      "CmdBase" -> "Tool";
      "Tool" -> "QTool";
      "QTool" -> "GUIToolBounds";
      "Tool" -> "CLToolBounds";
      "BaseToolBounds" -> "GUIToolBounds";
      "BaseToolBounds" -> "CLToolBounds";
      "CmdBase" -> "ToolBounds"
      "ToolBounds" -> "CLToolBounds" [style=dotted, label="CL", color=red, fontcolor=red];
      "ToolBounds" -> "GUIToolBounds" [style=dotted, label="GUI", color=red, fontcolor=red];
   }

Note for Victor regarding tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using a similar reasoning as with Applications, I suggest the following new structure:

.. graphviz::

   digraph foo {
      "CmdBase" [href="../developers/CodeCoreCL.html#cmdbase", target="_top"]
      "Tool" [href="../developers/CodeCoreCL.html#tool", target="_top"]
      "QTool" [href="../developers/CodeCoreGUI.html#qtool", target="_top", shape="box", style="rounded,filled"]
      "ToolBounds" [href="../developers/CodeTools.html#toolbounds", target="_top", shape=box, color=red]
      "BaseToolBounds" [href="../developers/CodeTools.html#toolbounds", target="_top"]
      "CLToolBounds" [href="../developers/CodeTools.html#toolbounds", target="_top"]
      "GUIToolBounds" [href="../developers/CodeTools.html#toolbounds", target="_top", shape="box", style="rounded,filled"]
      "CmdBase" -> "Tool";
      "Tool" -> "QTool";
      "QTool" -> "GUIToolBounds";
      "Tool" -> "BaseToolBounds";
      "BaseToolBounds" -> "CLToolBounds";
      "BaseToolBounds" -> "GUIToolBounds";
      "ToolBounds" -> "CLToolBounds" [style=dotted, label="CL", color=red, fontcolor=red];
      "ToolBounds" -> "GUIToolBounds" [style=dotted, label="GUI", color=red, fontcolor=red];
   }

Container Diagrams
==================

The structure RepTate, which can be clearly seen when running a CL or a GUI session, is also reflected in the code. Essentially:

   - A RepTate session may contain one or more open applications of the same or different type (*i.e.* LVE, NLVE, LAOS, etc).

   - Each application can have one or more open datasets (*i.e.* Set1, Set2, etc). Datasets are intended to group experimental data that are related in some way. For example:
   
      - SAOS measurements of samples of the same material, measured at same temperature, but having different molecular weight.

      - Start-up of shear flow measurements of samples of the same material and same molecular weight, measured at the same temperature, but with different shear rates. 

   - Each Dataset may contain one or several Data files, which are typically loaded from disk.

   - Inside each dataset, there may be one or more open theories of the same or different kind (*i.e.* Maxwell, Rouse, etc). Each theory is **only applied to the files in the same Dataset that contains the theory**.

   - Finally, each Application may have open tools of the same or different type (*i.e.* Find Peaks, Materials Database, etc). The tools are applied to **all the files in all the Datasets** contained in the same Application as the Tool. 

The following diagram shows a typical example of use of RepTate, representing the above structure in a schematic way. In the diagram:

   - The green box represents a RepTate session. 
   - In the session, there are three open applications (TTS1, LVE2 and NLVE3), represented by red rounded boxes.
   - Each application contains one or more datasets, represented by yellow folders. Some applications also have a tool, represented by a cyan arrow. 
   - Each dataset contains data files, represented in grey. In addition, some datasets have opened one or more theories, which are shown as purple boxes.

.. graphviz::

   digraph foo {
	  rankdir=LR
	  "RepTate" [shape="box",style="filled",fillcolor=mediumseagreen]
	  "TTS1" [shape="box",style="rounded,filled",fillcolor=indianred1]
	  "LVE2" [shape="box",style="rounded,filled",fillcolor=indianred1]
	  "NLVE3" [shape="box",style="rounded,filled",fillcolor=indianred1]
	  "Set1" [shape="folder",style="filled",fillcolor=khaki]
	  "Set2" [shape="folder",style="filled",fillcolor=khaki]
	  "Set3" [shape="folder",style="filled",fillcolor=khaki]
	  "Set4" [shape="folder",style="filled",fillcolor=khaki]
	  "WLF Shift" [shape="signature",style="filled",fillcolor=magenta1]
	  "Maxwell Modes" [shape="signature",style="filled",fillcolor=magenta1]
	  "Likhtman-McLeish" [shape="signature",style="filled",fillcolor=magenta1]
	  "PI88K 25C.osc" [shape="note",style="filled"]
	  "PI88K 10C.osc" [shape="note",style="filled"]
	  "PI94_T25.tts" [shape="note",style="filled"]
	  "PI225_T25.tts" [shape="note",style="filled"]
	  "dow150.shear" [shape="note",style="filled"]
	  "dow170.shear" [shape="note",style="filled"]
	  "hdpe320.shear" [shape="note",style="filled"]
	  "hdpe270.shear" [shape="note",style="filled"]
	  "Materials Database" [shape="cds",style="filled", fillcolor=cyan]
	  "Find Peaks" [shape="cds",style="filled", fillcolor=cyan]
      "RepTate" -> "TTS1";
      "RepTate" -> "LVE2";
      "RepTate" -> "NLVE3";
      "TTS1" -> "Set1";
      "Set1" -> "PI88K 25C.osc";
      "Set1" -> "PI88K 10C.osc";
      "Set1" -> "WLF Shift";
      "LVE2" -> "Set2";
      "Set2" -> "PI94_T25.tts";
      "Set2" -> "PI225_T25.tts";
      "Set2" -> "Maxwell Modes";
      "Set2" -> "Likhtman-McLeish";
      "LVE2" -> "Materials Database";
      "NLVE3" -> "Set3";
      "Set3" -> "dow150.shear";
      "Set3" -> "dow170.shear";
      "NLVE3" -> "Set4";
      "Set4" -> "hdpe320.shear";
      "Set4" -> "hdpe270.shear";
      "NLVE3" -> "Find Peaks"
   }

