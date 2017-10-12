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

print('Model: ' + model.findall(result.decode())[0] + '\n')
print('Firmware Revision: ' + firmware.findall(result.decode())[0] + '\n')
print('Serial Number: ' + serial_num.findall(result.decode())[0] + '\n')
print('Supported ATA Interfaces: ' + ata_interfaces.findall(result.decode())[0] + '\n')
print('DMA: ' + dma.findall(result.decode())[0] + '\n')
print('UDMA: ' + udma.findall(result.decode())[0] + '\n* (signifies the current active mode)\n')
print('PIO: ' + pio.findall(result.decode())[0] + '\n')

