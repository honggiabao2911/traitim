# heart_midautumn.py
# Hiệu ứng: Trái tim lấp lánh đập nhịp + vòng chữ chúc Trung Thu quay + hạt bay + nhạc nhac.mp3
# Chạy: pip install pygame  ->  python heart_midautumn.py

import math, random, os, sys, time
import pygame
import pygame.freetype

W, H = 900, 600
FPS = 60
BLACK = (0, 0, 0)

# --------- Helpers ----------
def load_music():
    try:
        pygame.mixer.init()
        if os.path.exists("nhac.mp3"):
            pygame.mixer.music.load("nhac.mp3")
            pygame.mixer.music.play(-1)
        else:
            print("⚠️ Không thấy nhac.mp3 — vẫn chạy không nhạc.")
    except Exception as e:
        print("⚠️ Không mở được nhạc:", e)

def try_load_font(size):
    # Ưu tiên font có tiếng Việt nếu bạn có trong thư mục dự án
    for fname in ["NotoSans-Regular.ttf", "Roboto-Regular.ttf", "Arial.ttf"]:
        if os.path.exists(fname):
            return pygame.freetype.Font(fname, size)
    # fallback: freetype default (có thể thiếu dấu tiếng Việt trên một số máy)
    return pygame.freetype.SysFont("Arial", size)

# Tạo điểm trên đường tim parametric
def heart_points(n=3500, scale=14.0):
    pts = []
    for _ in range(n):
        t = random.uniform(0, math.pi*2)
        x = 16*math.sin(t)**3
        y = 13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t)
        x, y = x/scale, y/scale
        pts.append([x, y, random.uniform(0.4, 1.0)])  # thêm độ sáng ngẫu nhiên
    return pts

def draw_glitter_heart(surf, center, pts, scale=1.0, pulse_alpha=1.0):
    cx, cy = center
    for x, y, b in pts:
        px = int(cx + x*200*scale)
        py = int(cy - y*200*scale)
        # lấp lánh: mỗi hạt có alpha riêng + dao động nhẹ
        a = max(0, min(255, int(220*b*(0.6 + 0.4*random.random())*pulse_alpha)))
        c = (180, 220, 255, a)  # xanh nhạt
        r = 1 if random.random() < 0.7 else 2
        glitter_dot(surf, (px, py), r, c)

def glitter_dot(surf, pos, r, color_rgba):
    dot = pygame.Surface((r*2+2, r*2+2), pygame.SRCALPHA)
    pygame.draw.circle(dot, color_rgba, (r+1, r+1), r)
    surf.blit(dot, (pos[0]-r-1, pos[1]-r-1))

# Particles bay lên
def init_particles(count=220):
    arr = []
    for _ in range(count):
        arr.append({
            "x": random.uniform(W*0.25, W*0.75),
            "y": random.uniform(H*0.70, H*0.98),
            "vx": random.uniform(-0.15, 0.15),
            "vy": random.uniform(-0.6, -1.4),
            "size": random.choice([1,1,1,2]),
            "hue": random.choice([(255,90,120),(255,150,170),(255,200,220),(240,240,255)])
        })
    return arr

def update_particles(particles):
    for p in particles:
        p["x"] += p["vx"] + math.sin(p["y"]*0.02)*0.02
        p["y"] += p["vy"]
        if p["y"] < H*0.20 or p["x"] < 0 or p["x"] > W:
            p["x"] = random.uniform(W*0.25, W*0.75)
            p["y"] = random.uniform(H*0.75, H*0.98)
            p["vx"] = random.uniform(-0.15, 0.15)
            p["vy"] = random.uniform(-1.2, -0.6)

def draw_particles(surf, particles):
    for p in particles:
        a = 140 if p["size"] == 2 else 100
        col = (*p["hue"], a)
        glitter_dot(surf, (int(p["x"]), int(p["y"])), p["size"], col)

# Vòng chữ quay
def draw_rotating_text_ring(surf, font, messages, base_angle_deg, radius_x, radius_y, center):
    cx, cy = center
    total = len(messages)
    for i, msg in enumerate(messages):
        ang = math.radians(base_angle_deg + i*(360/total))
        x = cx + math.cos(ang)*radius_x
        y = cy + math.sin(ang)*radius_y
        # render rồi xoay để nằm theo tiếp tuyến vòng tròn
        text_surf, _ = font.render(msg, (255,255,255))
        angle_text = -math.degrees(ang)  # xoay theo tiếp tuyến
        rot = pygame.transform.rotozoom(text_surf, angle_text, 1.0)
        rect = rot.get_rect(center=(x, y))
        surf.blit(rot, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Trung Thu – Trái tim lấp lánh")
    clock = pygame.time.Clock()
    random.seed()

    # Nhạc
    load_music()

    # Nền sao mờ
    starfield = pygame.Surface((W, H))
    starfield.fill(BLACK)
    for _ in range(450):
        x, y = random.randrange(W), random.randrange(H)
        col = random.randint(160, 255)
        starfield.set_at((x,y), (col, col, col))

    # Tim & hạt
    heart_pts = heart_points(n=4200, scale=14.0)
    particles = init_particles()

    # Font
    font_small = try_load_font(18)
    font_ring  = try_load_font(26)
    font_title = try_load_font(28)

    messages = [
        "Chúc Trung Thu ấm áp",
        "Vui vẻ – Đoàn viên",
        "Bình an – Hạnh phúc",
        "Trăng sáng – Lòng sáng",
        "Gia đình sum vầy",
        "Yêu thương trọn vẹn",
        "Rộn ràng tiếng cười",
        "Ngọt như bánh nướng"
    ]

    t0 = time.time()
    ring_angle = 0

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: running = False

        screen.blit(starfield, (0,0))

        # Nhịp tim (scale dao động nhẹ)
        t = time.time() - t0
        scale = 1.0 + 0.07*math.sin(t*2.2*math.pi)  # ~1.1 nhịp/giây
        pulse_alpha = 0.85 + 0.15*math.sin(t*4.4*math.pi)

        # Vẽ trái tim lấp lánh
        draw_glitter_heart(screen, (W//2, int(H*0.38)), heart_pts, scale=scale, pulse_alpha=pulse_alpha)

        # Hạt bay lên
        update_particles(particles)
        draw_particles(screen, particles)

        # Vòng chữ quay dưới
        ring_angle = (ring_angle + 0.5) % 360
        draw_rotating_text_ring(
            screen, font_ring, messages,
            base_angle_deg=ring_angle,
            radius_x=W*0.34, radius_y=H*0.08,
            center=(W//2, int(H*0.82))
        )

        # Tiêu đề nhỏ
        font_small.render_to(screen, (14, 14), "Nhấn ESC để thoát", (200,200,200))
        font_title.render_to(screen, (W//2-130, int(H*0.60)),
                             "Trung Thu an lành ✨", (255, 230, 200))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
