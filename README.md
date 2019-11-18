Example Output:
![](/finalOutput/exampleOne.gif)

The left animation is a top-down view, where the person's head is the black circle, with lines coming from their head representing their field of vision,
 and there are two red hands connected to the head.
The right animation is a profile view, used to detect whether they are looking up or down.

-----

BEFORE RUNNING:
Make sure that the following directories exist:
 1. dataLogs
 2. finalOutput
 3. intermediateFiles

Make sure to have the following python packages installed:
 imageio
 matplotlib

If you don't have the above python packages installed, one way they can be installed is to issue the following commands in your python environment:
 pip3 install imageio
 pip3 install matplotlib


TO RUN:
Place your *.csv files into the dataLogs/ directory, then run the visualizeData.py script.  Example runs have been included, as well as example final
outputs.  One has been left un-run for convenience in testing.

FINAL RESULT:
The result is a *.gif animation of the data collection session that shows two views.  
The left animation is a top-down view, where the person's head is the black circle, with lines coming from their head representing their field of vision,
 and there are two red hands connected to the head.
The right animation is a profile view, used to detect whether they are looking up or down.
