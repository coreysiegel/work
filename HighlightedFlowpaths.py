import csv
import argparse
import re
import sys

parser = argparse.ArgumentParser(description='Produce Adobe Acrobat Javascript source to combine P&IDs for highlighted flowpaths.  ' + \
		'Drawings will be annotated with operation, step, and (if applicable) sub-step information.')
parser.add_argument('vShift', help='Pixels to shift from the left side (after rotation)')
parser.add_argument('hShift', help='Pixels to shift from the top side (after rotation)')
parser.add_argument('input', help='Input CSV file with list of P&IDs for each operation/step/sub-step')

args = parser.parse_args()
if args.input[-1:] == '\r':
	args.input=args.input[:-1]
sys.stderr.write('input=' + args.input + '\n')
sys.stderr.write('vShift=' + args.vShift + '\n')
sys.stderr.write('hShift=' + args.hShift + '\n')

vShift=args.vShift
hShift=args.hShift

with open(args.input, 'r') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',')
	rowID=0
	for row in csvreader:
		if len(row) < 6:
			exit
		if rowID!=0:
			if rowID==1:
				operation=row[0]
				fcn_name='HighlightedFlowpaths_'+''.join(re.findall(r"[\w]+", operation))
				print('function '+fcn_name+'()')
				print('{')
				print('	if (this.numPages > 1) this.deletePages({nStart:1, nEnd:this.numPages-1});')
			print('	this.insertPages({nPage:this.numPages-1, cPath:"U:\\\\184200669\\\\process\\\\drawing\\\\PID\\\\PID-' + row[5] + '.pdf"});')
			if len(row[3]) > 0:
				print('	this.addWatermarkFromText({cText: "Highlighted Flowpath for Operation ' + \
					row[0] + ', Step ' + row[1] + ': ' + row[2] + ', Sub-Step ' + row[3] + ': ' + row[4] + \
					'", nHorizAlign:app.constants.align.right, nHorizValue: -' + str(hShift) + ', nVertAlign:app.constants.align.top, nVertValue: -' + str(vShift) + ', cFont: "Arial", nFontSize:16, nStart: ' + str(rowID) + ', nRotation: -90});')
			else:
				print('	this.addWatermarkFromText({cText: "Highlighted Flowpath for Operation ' + \
					row[0] + ', Step ' + row[1] + ': ' + row[2] + \
					'", nHorizAlign:app.constants.align.right, nHorizValue: -' + str(hShift) + ', nVertAlign:app.constants.align.top, nVertValue: -' + str(vShift) + ', cFont: "Arial", nFontSize:16, nStart: ' + str(rowID) + ', nRotation: -90});')
		rowID = rowID + 1
print('app.alert({cMsg:"Process complete.",nIcon:3,cTitle:"' + fcn_name + '"})')
print('}')
print('app.addMenuItem({')
print('	cName: "' + operation + ' Highlighted Flowpaths",')
print('	cParent: "Edit",')
print('	cExec: "'+fcn_name+'()"')
print('});')
