import pygame
import os
import glob
from settings import *

tracking = {
}
gl_summon_sprites = []
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
    global gl_summon_sprites
    if len(gl_summon_sprites) > 0:
        return gl_summon_sprites
    file_path = "assets/image/backup_summon"
    file_list = list(os.listdir(file_path))
    file_list = sorted(file_list)
    summon_sprites = []
    for file in file_list:
        if not file.endswith(".png"):
            continue
        real_file = os.path.join(file_path, file)
        if os.path.exists(real_file): 
            img = pygame.image.load(real_file).convert_alpha()
            summon_sprites.append(pygame.transform.scale(img, (size/1.4, size/1.4)))
        else:
            print(f"Lỗi: Không tìm thấy file {real_file}")
    gl_summon_sprites = summon_sprites
    return summon_sprites



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

def tint_add(image, color):
    """Additive color tint"""
    tinted = image.copy()
    tinted.fill(color, special_flags=pygame.BLEND_RGB_ADD)
    return tinted

# Bước 3: Nạp tài nguyên (Sau khi đã có screen)
# Lưu ý: Tôi điều chỉnh lại range để không bị trùng lặp các frame
# try:
    
# except Exception as e:
    