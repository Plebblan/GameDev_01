import pygame
import os
import glob

def load_zombie_frames(prefix, state, size = 85):
    frames = []
    file_path = f"{prefix}/{state}"
    for file in os.listdir(file_path):
        if not file.endswith(".png"):
            continue
        real_file = os.path.join(file_path, file)
        if os.path.exists(real_file): 
            img = pygame.image.load(real_file).convert_alpha()
            original_rect = img.get_rect()
            frames.append(pygame.transform.scale(img, (original_rect.width / original_rect.height * size, size)))
        else:
            print(f"Lỗi: Không tìm thấy file {real_file}")
    return frames

# Bước 3: Nạp tài nguyên (Sau khi đã có screen)
# Lưu ý: Tôi điều chỉnh lại range để không bị trùng lặp các frame
# try:
    
# except Exception as e:
    