import pygame
import os

def load_zombie_frames(prefix, start, end, size = 85):
    frames = []
    for i in range(start, end):
        file_path = f"{prefix}{i:04}.png"
        if os.path.exists(file_path): # Kiểm tra file có tồn tại không
            img = pygame.image.load(file_path).convert_alpha()
            frames.append(pygame.transform.scale(img, (size, size)))
        else:
            print(f"Lỗi: Không tìm thấy file {file_path}")
    return frames

# Bước 3: Nạp tài nguyên (Sau khi đã có screen)
# Lưu ý: Tôi điều chỉnh lại range để không bị trùng lặp các frame
# try:
    
# except Exception as e:
    