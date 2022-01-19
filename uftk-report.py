# coding=utf-8

import sys
import xml.etree.ElementTree
from subprocess import run
from pathlib import Path

def unpack_uftk(container_path):

    container_filename = str(container_path)
    container_id       = container_filename[:-4]
    unpack_cl = '7z e \"{0}\" -o\"{1}\" -y'.format(container_filename,
                                                   container_id)
    run(unpack_cl)
    
    package_description = container_path.parent \
                                        .joinpath(container_id) \
                                        .joinpath('packageDescription.xml')
    
    return(package_description)
    
def read_description(description_path):

    tree = xml.etree.ElementTree.parse(description_path)
    root = tree.getroot()
    
    for document in root.iter('документ'):
        
        document_code = document.attrib['кодТипаДокумента']
    
        if document_code == '01':
        
            main_file_name = document.attrib['исходноеИмяФайла']
    
        sender = root.find('отправитель')
    
        sender_ip = sender.attrib['адрес']
        
    tr_info = [main_file_name, sender_ip]
        
    return(tr_info)
    

work_path = Path(sys.argv[1])

containers_list = list(work_path.rglob('*.zip'))

log_file_path = work_path.joinpath('result.txt')

log_file = open(log_file_path, 'w')

for current_container in containers_list:
    
    current_description = unpack_uftk(current_container)
    
    current_tr_info = read_description(current_description)

    result_line = current_tr_info[0] + '\t' + current_tr_info[1]
    
    log_file.write(result_line + '\n')
    
    print(result_line)
    
log_file.close()