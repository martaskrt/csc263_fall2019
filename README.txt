Dependencies:
Python3 pandas:
pip3 install pandas

Python3 numpy (fully uninstall before installing):
pip3 uninstall numpy
pip3 install numpy

To run:
1. Download the quercus gradebook:
	Quercus -> Grades -> Actions -> Export

2. Export the Crowdmark grades:
	My Courses -> 'this course' -> 'an assignment' -> Result -> Export grades as a CSV

3. Put all the downloaded files in a subdirectory

4. In the subdirectory, make a file called 'assignment_list.csv' with the following format:

Quercus Assignment,Crowdmark File,Deadline
Problem Set 1 (230306),problem-set-1-e3941-marks.csv,2019-09-17 22:00:00
Problem Set 2 (232908),problem-set-2-4f1b9-marks.csv,2019-09-24 22:00:00
Problem Set 3 (238527),problem-set-3-16f75-marks.csv,2019-10-08 22:00:00
Problem Set 4 (239487),problem-set-4-ed7e5-marks.csv,2019-10-15 22:00:00
Problem Set 5 (255715),problem-set-5-3c8c5-marks.csv,2019-11-12 22:00:00
Problem Set 7 (255716),problem-set-7-8f96d-marks.csv,2019-11-26 22:00:00

	Note that it is tab separated, not comma separated (for compatibility with quercus gradebooks).
	The first column has the names of the assignments as listed in the Quercus gradebook header (see step 1.)
	The second column has the names of the corresponding grades files from Crowdmark (see step 2.)
	The third column has the assignment's due date formatted as 'YYYY-MM-DD HH:MM:SS' in the local timezone
		(python datetime and dateutil handle timezones and time changes)

5. In calculate_lateness.py the function 'lateness_function' calculates the percentage penalty based on the
	the students' submission time and the deadline.

6. In calculate_lateness.py, line 52 automatically generates the filename for the quercus gradebook
	we've had some trouble with it, so we've had to hardcode the filename on line 53

7. In the main directory run:
	$python3 calculate_lateness.py --dir {subdirectory}

	where {subdirectory is the name of the directory containing the csv files specific to your course.

	The script will generate a new quercus gradebook with the same title albeit '_updated' appended before the file extension.
	This gradebook will have the columns reordered, with the newly adjusted grades columns at the end.

	The other columns will remain unchanged in the gradebook. Do not upload it to quercus as is.



