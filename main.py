from adrv.main import Disk, Size, Converter
import os

convert = Converter().convert

personnal = Disk('./disks/personnal.adrv', convert(50, "kB", "B")) # Creates a 12MB virtual disk

with open('data/drawing.png', 'rb') as _file: # Open an existing file...
	personnal.write(_file.read(), '/images', 'img1.png') # ...and copy it into the VDisk

with open('data/note.txt', 'r') as _file: # It works for text as well
	amount_written = personnal.write(_file.read(), '/text', 'note.txt') # And you can collect the amount of bytes written on the disk.
	print(f"{Size(amount_written).literal()} have been written.")

with open('data/drawing2.png', 'rb') as _file:
	personnal.write(_file.read(), '/images', 'img2.png')

percentageUsed = round(personnal.size.raw / personnal.max_size.raw * 10000) / 100
print(f"{'None' if percentageUsed == 0 else f'{percentageUsed}%'} of the storage used ({personnal.size.literal()} out of {personnal.max_size.literal()})")

drawing1 = personnal.open_file('/images/img1.png')
drawing2 = personnal.open_file('/images/img2.png')
note = personnal.open_file('/text/note.txt')


try:
	os.makedirs('dist/')
except:
	pass


with open('dist/drawing.png', 'wb') as file:
	file.write(drawing1.content)
	personnal.remove('/images/img1.png')

with open('dist/drawing2.png', 'wb') as file:
	file.write(drawing2.content)
	personnal.remove('/images/img2.png')

with open('dist/note.txt', 'wb') as file:
	file.write(note.content)
	personnal.remove('/text/note.txt')

percentageUsed = round(personnal.size.raw / personnal.max_size.raw * 10000) / 100
print(f"{'None' if percentageUsed == 0 else f'{percentageUsed}%'} of the storage used ({personnal.size.literal()} out of {personnal.max_size.literal()})")