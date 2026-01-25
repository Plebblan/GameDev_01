import pygame
import sys

# Allowed 16:9 resolutions
RESOLUTIONS = [
    (640, 360),
    (800, 450),
    (960, 540),
    (1120, 630),
    (1280, 720),
    (1440, 810),
    (1600, 900),
]

DIFFICULTIES = ["Easy", "Normal", "Hard"]
TEXTBOX_SCALE = 1.2

def menu(screen,background):
    clock = pygame.time.Clock()

    background = background

    bg_w, bg_h = screen.get_size()
    background = pygame.transform.smoothscale(
        background, (bg_w, bg_h)
    )

    # Load assets
    textbox = pygame.image.load(
        "assets/image/menu.png"
    ).convert_alpha()

    tb_w, tb_h = textbox.get_size()
    textbox = pygame.transform.smoothscale(
        textbox,
        (int(tb_w * TEXTBOX_SCALE), int(tb_h * TEXTBOX_SCALE))
    )

    font_title = pygame.font.Font(
        "assets/font/Brianne_s_hand.ttf", 34
    )
    font_text = pygame.font.Font(
        "assets/font/Brianne_s_hand.ttf", 26
    )
    font_button = pygame.font.Font(
        "assets/font/Brianne_s_hand.ttf", 28
    )

    res_index = 0
    diff_index = 1
    selection = 0  # 0 = resolution, 1 = difficulty

    base_w, base_h = screen.get_size()
    textbox_rect = textbox.get_rect(center=(base_w // 2, base_h // 2))

    padding_top = 30
    row_gap = 40

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selection = (selection - 1) % 2
                if event.key == pygame.K_DOWN:
                    selection = (selection + 1) % 2
                if event.key == pygame.K_LEFT:
                    if selection == 0:
                        res_index = (res_index - 1) % len(RESOLUTIONS)
                    else:
                        diff_index = (diff_index - 1) % len(DIFFICULTIES)
                if event.key == pygame.K_RIGHT:
                    if selection == 0:
                        res_index = (res_index + 1) % len(RESOLUTIONS)
                    else:
                        diff_index = (diff_index + 1) % len(DIFFICULTIES)
                if event.key == pygame.K_RETURN:
                    return RESOLUTIONS[res_index], DIFFICULTIES[diff_index]

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if res_rect.collidepoint(mouse_pos):
                    selection = 0
                elif diff_rect.collidepoint(mouse_pos):
                    selection = 1
                elif left_arrow.collidepoint(mouse_pos):
                    if selection == 0:
                        res_index = (res_index - 1) % len(RESOLUTIONS)
                    else:
                        diff_index = (diff_index - 1) % len(DIFFICULTIES)
                elif right_arrow.collidepoint(mouse_pos):
                    if selection == 0:
                        res_index = (res_index + 1) % len(RESOLUTIONS)
                    else:
                        diff_index = (diff_index + 1) % len(DIFFICULTIES)
                elif start_rect.collidepoint(mouse_pos):
                    return RESOLUTIONS[res_index], DIFFICULTIES[diff_index]

        screen.blit(background, (0, 0))
        screen.blit(textbox, textbox_rect)

        title = font_title.render("Options", True, (255, 255, 255))
        screen.blit(
            title,
            title.get_rect(centerx=base_w // 2, top=textbox_rect.top + padding_top)
        )

        res_color = (255, 220, 120) if selection == 0 else (200, 200, 200)
        res_text = font_text.render(
            f"Resolution: {RESOLUTIONS[res_index][0]} x {RESOLUTIONS[res_index][1]}",
            True, res_color
        )
        res_rect = res_text.get_rect(
            centerx=base_w // 2,
            centery=textbox_rect.centery - row_gap
        )
        screen.blit(res_text, res_rect)

        diff_color = (255, 220, 120) if selection == 1 else (200, 200, 200)
        diff_text = font_text.render(
            f"Difficulty: {DIFFICULTIES[diff_index]}",
            True, diff_color
        )
        diff_rect = diff_text.get_rect(
            centerx=base_w // 2,
            centery=textbox_rect.centery
        )
        screen.blit(diff_text, diff_rect)

        arrow_y = res_rect.centery if selection == 0 else diff_rect.centery

        left = font_text.render("<", True, (220, 220, 220))
        right = font_text.render(">", True, (220, 220, 220))

        left_arrow = left.get_rect(
            center=(textbox_rect.left + 60, arrow_y)
        )
        right_arrow = right.get_rect(
            center=(textbox_rect.right - 60, arrow_y)
        )

        screen.blit(left, left_arrow)
        screen.blit(right, right_arrow)

        start_text = font_button.render("START", True, (255, 255, 255))
        start_rect = start_text.get_rect(
            centerx=base_w // 2,
            bottom=textbox_rect.bottom - 35
        )
        screen.blit(start_text, start_rect)

        pygame.display.flip()
        clock.tick(60)