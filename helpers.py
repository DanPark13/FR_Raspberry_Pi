# Helper functions used in processing main and camera

from datetime import datetime
import itertools
import operator

# Gets the most common element in a list
def most_common(L):
	# get an iterable of (item, iterable) pairs
	SL = sorted((x, i) for i, x in enumerate(L))
	# print 'SL:', SL
	groups = itertools.groupby(SL, key=operator.itemgetter(0))
	# auxiliary function to get "quality" for an item
	def _auxfun(g):
		item, iterable = g
		count = 0
		min_index = len(L)
		for _, where in iterable:
			count += 1
			min_index = min(min_index, where)
		# print 'item %r, count %r, minind %r' % (item, count, min_index)
		return count, -min_index
	# pick the highest-count/earliest item
	return max(groups, key=_auxfun)[0]

# Write the person's name down in the attendance sheet when identified on webcam
def mark_attendance(person_name):
    with open("attendance_sheet.csv", "r+") as sheet:
        current_data_list = sheet.readlines()
        name_list = []
        
        # Create a new entry
        for line in current_data_list:
            entry = line.split(",")
            name_list.append(entry[0])
            
        # If person detected is not in the attendance sheet, mark them in the sheet
        if person_name not in name_list:
            time_now = datetime.now()
            date = time_now.strftime("%x")
            time = time_now.strftime("%H:%M:%S")
            sheet.writelines(f"\n{person_name},{date},{time}")
