import subprocess
import re
import shlex

result = subprocess.check_output(['hdparm', '-i', "/dev/sda"])
ata_interfaces = re.compile('ATA.*')
model = re.compile('(?<=Model=).*(?=, FwRe)')
firmware = re.compile('(?<=FwRev=).*(?=,)')
serial_num = re.compile('(?<=SerialNo=).*')
dma = re.compile('(?<=DMA modes: {2}).*')
udma = re.compile('(?<=UDMA modes: ).*')
pio = re.compile('(?<=PIO modes: {2}).*')

total_space_result = subprocess.check_output(['hdparm', '-I', "/dev/sda"])
total_size_regex = re.compile('(?<=\tdevice size with M = 1024\*1024: {6}).*(?= MBytes)')
total_size = int(total_size_regex.findall(total_space_result.decode())[0])


free_space_result = subprocess.Popen(shlex.split('df -m'), stdout=subprocess.PIPE)
searched = subprocess.Popen(shlex.split('grep ' + "/dev/sda"), stdin=free_space_result.stdout, stdout=subprocess.PIPE)
awked = subprocess.Popen(shlex.split('awk \'{print $4}\''), stdin=searched.stdout, stdout=subprocess.PIPE)
out = awked.communicate()
total_free = 0
for free in out[0].decode().split():
    total_free += int(free)

print('Model: ' + model.findall(result.decode())[0] + '\n')
print('Firmware Revision: ' + firmware.findall(result.decode())[0] + '\n')
print('Serial Number: ' + serial_num.findall(result.decode())[0] + '\n')
print('Supported ATA Interfaces: ' + ata_interfaces.findall(result.decode())[0] + '\n')
print('DMA: ' + dma.findall(result.decode())[0] + '\n')
print('UDMA: ' + udma.findall(result.decode())[0] + '\n* (signifies the current active mode)\n')
print('PIO: ' + pio.findall(result.decode())[0] + '\n')
print("Total space: " + str(total_size) + ' MBytes')
print('Used and unavailable to access from this system: ' + str(total_size - total_free) + " MBytes")
print('Free: ' + str(total_free) + " MBytes")
