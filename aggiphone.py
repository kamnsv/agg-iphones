from PIL import Image
import os
import sys
import shutil
from videoprops import get_video_properties
from datetime import datetime as dt
import subprocess

OFFSET = dt.now() - dt.utcnow()
DIRJPG = '.tmp_heic_to_jpg'
DIRDIST = sys.argv[2] or 'common'

def get_date_photo_taken(fname):
    data = Image.open(fname)._getexif()
    if not data: return
    try:
        date_photo_taken = data[36867]
    except: 
        #print(data)
        return
    return date_photo_taken.replace(':','-').replace(' ','_')[:19]

def get_date_mov_taken(fname):
    props = get_video_properties(fname)
    try:
        utc = props['tags']['creation_time'][:19]
        loc = dt.strptime(utc, '%Y-%m-%dT%H:%M:%S' if 'T' in utc else '%Y-%m-%d %H:%M:%S' ) + OFFSET
        return str(loc).replace(':','-').replace(' ','_')[:19]
    except: 
        #print(props)
        return 
    
    
def convert_heic_to_jpg(path):
   
    os.makedirs(DIRJPG, exist_ok = True)
    new_path = DIRJPG + '/' + os.path.basename(path) + '.jpg'
    try:
        os.remove(new_path)
    except: pass
    
    cmd = f'heif-convert -q 100 {path} {new_path}'
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return new_path

def main():
    os.makedirs(DIRDIST, exist_ok = True)	
    count, err = 0, 0
    for root, dirs, files in os.walk(sys.argv[1]):
        for fname in files:
            # Очередной файл
            path = os.path.join(root, fname)
            
            data = None # данные о дате съемки
            sub = '' # подкаталог 
            errstr = '' # текст ошибки 
            tag = path.split(os.sep)[1] # тег имени нового файла 
            
            # Определяем дату съемки фото или видео
            
            try:
                if fname.lower().endswith(".png"):
                    data = get_date_photo_taken(path)

                if fname.lower().endswith(".jpg"):
                    data = get_date_photo_taken(path)

                if fname.lower().endswith(".mp4"):
                    data = get_date_mov_taken(path)

                if fname.lower().endswith(".mov"):
                    data = get_date_mov_taken(path)
                    
                if fname.lower().endswith(".heic"):
                    path = convert_heic_to_jpg(path)
                    data = get_date_photo_taken(path)
                
                if data is None:
                    errstr = ''
                    
            except Exception as e:
                errstr = str(e) + ' ' + repr(e)  
                
           
            if data is None:   # Если не получили дату съeмки
                err += 1
                print('error path:', path, '; text error:', errstr)
                continue
            else:  # Определяем подпапку по дате съeмки
                sub = data.split('_')[0][:7] # год-месяц
                os.makedirs(os.path.join(DIRDIST, sub), exist_ok = True)
                
            # Определяем новое имя
            target = data + '_' + tag + os.path.splitext(path)[1].lower()
            path_target = os.path.join(DIRDIST, sub, target)
            
            
            # Удаляем старый файл если он меньше весом
            if os.path.isfile(path_target):
                if os.stat(path_target).st_size < os.stat(path).st_size:
                    os.remove(path_target)
                else:
                    continue
                    
            # Копируем
            shutil.copy(path, path_target)
            count += 1    
 
            print(count, path,'to',path_target, end='\r')
            
    print('/nCopy file:', count, 'Errors:', err)
    os.system(f'rm -rf {DIRJPG}')   

if len(sys.argv) > 1:
    main()
            