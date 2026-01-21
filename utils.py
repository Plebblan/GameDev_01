import pygame
import os
import glob
from settings import *

tracking = {
}
dirt_sprites = []
zom_frame = None
def load_zombie_frames(prefix="assets/image/basic", state="move", size = 60):
    frames = tracking.get(prefix + state, [])
    if len(frames) > 0:
        return frames
    file_path = f"{prefix}/{state}"
    file_list = list(os.listdir(file_path))
    file_list = sorted(file_list)
    for file in file_list:
        if not file.endswith(".png"):
            continue
        real_file = os.path.join(file_path, file)
        if os.path.exists(real_file): 
            img = pygame.image.load(real_file).convert_alpha()
            original_rect = img.get_rect()
            frames.append(pygame.transform.scale(img, (size, size)))
        else:
            print(f"Lỗi: Không tìm thấy file {real_file}")
    tracking[prefix + state] = frames
    return frames

def create_summon_sprites(size = 60):
    global zom_frame
    if len(dirt_sprites) > 0:
        return (dirt_sprites, zom_frame)
    file_path = "assets/image/dirt_animation"
    file_list = list(os.listdir(file_path))
    file_list = sorted(file_list)
    for file in file_list:
        if not file.endswith(".png"):
            continue
        real_file = os.path.join(file_path, file)
        if os.path.exists(real_file): 
            img = pygame.image.load(real_file).convert_alpha()
            dirt_sprites.append(pygame.transform.scale(img, (size/8, size/8)))
        else:
            print(f"Lỗi: Không tìm thấy file {real_file}")
    file_path_zom = "assets/image/creep_backup/move/gotybackup0039.png"
    if os.path.exists(file_path_zom):
        img = pygame.image.load(real_file).convert_alpha()
        frame = pygame.transform.scale(img, (size, size))
        zom_frame = frame
    else:
            print(f"Lỗi: Không tìm thấy file {file_path_zom}")
    return (dirt_sprites, frame)



def load_hammer_frames(directory, size=(BASE_HAMMER, BASE_HAMMER)):
    file_list = list(os.listdir(directory))
    file_list = sorted(file_list, key=lambda x: (len(x), x))
    frames = []
    for file in file_list:
        if not file.endswith(".png"):
            continue
        real_file = os.path.join(directory, file)
        if os.path.exists(real_file):
            img = pygame.image.load(real_file).convert_alpha()
            frames.append(pygame.transform.smoothscale(img, size))
        else:
            print(f"File {real_file} not exist")
    
    return frames

# Bước 3: Nạp tài nguyên (Sau khi đã có screen)
# Lưu ý: Tôi điều chỉnh lại range để không bị trùng lặp các frame
# try:
    
# except Exception as e:
    