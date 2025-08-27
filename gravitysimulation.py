import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Screen dimensions - wider and taller
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bounce Simulation with Velocity Control")

# Colors
BACKGROUND = (15, 25, 35)
BALL_COLOR = (255, 100, 100)
GROUND_COLOR = (70, 120, 80)
UI_BACKGROUND = (40, 50, 60)
TEXT_COLOR = (220, 220, 220)
VELOCITY_COLOR = (100, 220, 255)
TRAIL_COLOR = (255, 150, 150, 100)
SLIDER_COLOR = (100, 150, 200)
SLIDER_HANDLE = (230, 200, 100)
DRAG_LINE_COLOR = (255, 255, 100)
BUTTON_COLOR = (80, 180, 80)
BUTTON_HOVER_COLOR = (100, 200, 100)
TITLE_COLOR = (255, 215, 0)

# Ball properties
ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 4
ball_vel_y = 0
ball_vel_x = 0

# Physics properties
gravity = 9.8  # Earth gravity in m/s²
elasticity = 0.8  # Energy retention after bounce
ground_height = HEIGHT - 100
time_step = 0.1  # Simulation time step

# UI properties
slider_x = 150
slider_y = HEIGHT - 50
slider_width = WIDTH - 300
slider_height = 8
slider_handle_radius = 12
min_gravity = 1.0
max_gravity = 25.0

# Fonts
font = pygame.font.SysFont('Arial', 18)
title_font = pygame.font.SysFont('Arial', 24, bold=True)
large_font = pygame.font.SysFont('Arial', 36, bold=True)

# Physics data tracking
max_bounce_height = 0
bounce_count = 0
simulation_time = 0
is_dragging = False
drag_start_x, drag_start_y = 0, 0
ball_trail = []
paused = False
show_opening_screen = True
opening_screen_time = 0

def reset_ball():
    """Reset ball to initial position"""
    global ball_x, ball_y, ball_vel_y, ball_vel_x, max_bounce_height, bounce_count, simulation_time, ball_trail
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 4
    ball_vel_y = 0
    ball_vel_x = 0
    max_bounce_height = 0
    bounce_count = 0
    simulation_time = 0
    ball_trail = []

def draw_ball():
    """Draw the ball with a simple shading effect"""
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_x), int(ball_y)), ball_radius)
    # Add a highlight
    pygame.draw.circle(screen, (255, 180, 180), (int(ball_x - ball_radius//3), int(ball_y - ball_radius//3)), ball_radius//3)

def draw_ball_trail():
    """Draw a trail behind the ball to show its path"""
    for i, (trail_x, trail_y) in enumerate(ball_trail):
        # Make older trail points more transparent
        alpha = max(0, 150 - i * 3)
        if alpha > 0:
            trail_surf = pygame.Surface((ball_radius*2, ball_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, (*TRAIL_COLOR[:3], alpha), (ball_radius, ball_radius), ball_radius * (0.5 + 0.5 * i/len(ball_trail)))
            screen.blit(trail_surf, (trail_x - ball_radius, trail_y - ball_radius))

def draw_velocity_vector():
    """Draw a vector showing the ball's velocity"""
    if abs(ball_vel_x) > 0.1 or abs(ball_vel_y) > 0.1:
        # Scale the velocity for visualization
        scale = 0.5
        end_x = ball_x + ball_vel_x * scale
        end_y = ball_y + ball_vel_y * scale
        
        # Draw the velocity vector line
        pygame.draw.line(screen, VELOCITY_COLOR, (ball_x, ball_y), (end_x, end_y), 3)
        
        # Draw arrowhead
        angle = math.atan2(end_y - ball_y, end_x - ball_x)
        arrow_size = 10
        pygame.draw.polygon(screen, VELOCITY_COLOR, [
            (end_x, end_y),
            (end_x - arrow_size * math.cos(angle - math.pi/6), end_y - arrow_size * math.sin(angle - math.pi/6)),
            (end_x - arrow_size * math.cos(angle + math.pi/6), end_y - arrow_size * math.sin(angle + math.pi/6))
        ])
        
        # Display velocity magnitude
        velocity_mag = math.sqrt(ball_vel_x**2 + ball_vel_y**2)
        vel_text = font.render(f"{velocity_mag:.1f} m/s", True, VELOCITY_COLOR)
        screen.blit(vel_text, (end_x + 5, end_y - 10))

def draw_drag_line():
    """Draw a line when dragging to set initial velocity"""
    if is_dragging:
        # Draw line from ball to mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.line(screen, DRAG_LINE_COLOR, (ball_x, ball_y), (mouse_x, mouse_y), 2)
        
        # Draw arrowhead at mouse position
        angle = math.atan2(mouse_y - ball_y, mouse_x - ball_x)
        arrow_size = 10
        pygame.draw.polygon(screen, DRAG_LINE_COLOR, [
            (mouse_x, mouse_y),
            (mouse_x - arrow_size * math.cos(angle - math.pi/6), mouse_y - arrow_size * math.sin(angle - math.pi/6)),
            (mouse_x - arrow_size * math.cos(angle + math.pi/6), mouse_y - arrow_size * math.sin(angle + math.pi/6))
        ])
        
        # Calculate and display the velocity that would be applied
        dx = mouse_x - ball_x
        dy = mouse_y - ball_y
        velocity = math.sqrt(dx**2 + dy**2) / 10  # Scale for reasonable values
        angle_deg = math.degrees(math.atan2(-dy, dx)) % 360
        
        vel_text = font.render(f"Velocity: {velocity:.1f} m/s at {angle_deg:.0f}°", True, DRAG_LINE_COLOR)
        screen.blit(vel_text, (mouse_x + 10, mouse_y))

def draw_ground():
    """Draw the ground with some texture"""
    pygame.draw.rect(screen, GROUND_COLOR, (0, ground_height, WIDTH, HEIGHT - ground_height))
    
    # Add some ground texture
    for i in range(0, WIDTH, 15):
        pygame.draw.line(screen, (60, 110, 70), (i, ground_height), (i, HEIGHT), 1)
    
    # Ground border
    pygame.draw.line(screen, (50, 90, 60), (0, ground_height), (WIDTH, ground_height), 3)

def draw_ui():
    """Draw the user interface"""
    # Draw UI background
    pygame.draw.rect(screen, UI_BACKGROUND, (0, HEIGHT - 90, WIDTH, 90))
    
    # Draw slider
    pygame.draw.rect(screen, SLIDER_COLOR, (slider_x, slider_y - slider_height//2, slider_width, slider_height))
    
    # Calculate slider handle position
    handle_x = slider_x + (gravity - min_gravity) / (max_gravity - min_gravity) * slider_width
    pygame.draw.circle(screen, SLIDER_HANDLE, (int(handle_x), slider_y), slider_handle_radius)
    
    # Draw slider text
    gravity_text = font.render(f"Gravity: {gravity:.2f} m/s²", True, TEXT_COLOR)
    screen.blit(gravity_text, (slider_x, slider_y - 30))
    
    min_text = font.render(f"{min_gravity}", True, TEXT_COLOR)
    screen.blit(min_text, (slider_x - 20, slider_y + 10))
    
    max_text = font.render(f"{max_gravity}", True, TEXT_COLOR)
    screen.blit(max_text, (slider_x + slider_width - 20, slider_y + 10))
    
    # Draw title
    title = title_font.render("Ball Bounce Simulation with Velocity Control", True, TEXT_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))

def draw_stats():
    """Draw simulation statistics"""
    # Draw stats box
    stats_rect = pygame.Rect(WIDTH - 250, 60, 230, 180)
    pygame.draw.rect(screen, UI_BACKGROUND, stats_rect)
    pygame.draw.rect(screen, TEXT_COLOR, stats_rect, 2)  # Border
    
    # Draw stats text
    velocity_mag = math.sqrt(ball_vel_x**2 + ball_vel_y**2)
    angle_deg = math.degrees(math.atan2(-ball_vel_y, ball_vel_x)) % 360 if velocity_mag > 0.1 else 0
    
    stats_text = [
        f"Gravity: {gravity:.2f} m/s²",
        f"Bounce count: {bounce_count}",
        f"Max height: {max_bounce_height:.2f} m",
        f"Velocity: {velocity_mag:.2f} m/s",
        f"Angle: {angle_deg:.1f}°",
        f"Vx: {ball_vel_x:.2f} m/s",
        f"Vy: {ball_vel_y:.2f} m/s",
        f"Time: {simulation_time:.1f} s"
    ]
    
    for i, text in enumerate(stats_text):
        stat = font.render(text, True, TEXT_COLOR)
        screen.blit(stat, (WIDTH - 240, 70 + i * 22))
    
    # Draw pause indicator
    if paused:
        pause_text = font.render("PAUSED - You can adjust velocities", True, (255, 100, 100))
        screen.blit(pause_text, (WIDTH - 240, 70 + 8 * 22))

def draw_pause_button():
    """Draw the pause/play button"""
    button_rect = pygame.Rect(20, HEIGHT - 85, 100, 30)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hover = button_rect.collidepoint(mouse_x, mouse_y)
    
    # Draw button
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR if hover else BUTTON_COLOR, button_rect, border_radius=5)
    
    # Draw button text
    button_text = font.render("Pause" if not paused else "Play", True, TEXT_COLOR)
    screen.blit(button_text, (button_rect.centerx - button_text.get_width()//2, 
                             button_rect.centery - button_text.get_height()//2))
    
    return button_rect

def draw_opening_screen():
    """Draw the opening screen with title and creator name"""
    # Fade effect based on time
    alpha = min(255, max(0, 255 - (opening_screen_time - 3000) / 10))
    
    # Draw background
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    # Draw title
    title = large_font.render("Ball Bounce Simulation", True, TITLE_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
    
    # Draw creator name
    creator = title_font.render("Fun Project by Sahan Rashmika", True, TEXT_COLOR)
    screen.blit(creator, (WIDTH//2 - creator.get_width()//2, HEIGHT//2 - 30))
    
    # Draw instructions
    instructions = [
        "Click and drag the ball to set initial velocity",
        "Adjust the slider to change gravity",
        "Press R to reset, SPACE for random velocity",
        "Press P to pause and adjust velocities",
        "Click anywhere to start..."
    ]
    
    for i, text in enumerate(instructions):
        instruction = font.render(text, True, TEXT_COLOR)
        screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//2 + 40 + i * 30))
    
    # Draw bouncing ball animation
    bounce_time = opening_screen_time / 1000
    bounce_y = HEIGHT//2 - 200 + abs(math.sin(bounce_time * 2)) * 100
    bounce_x = WIDTH//2 + math.sin(bounce_time) * 100
    
    pygame.draw.circle(screen, BALL_COLOR, (int(bounce_x), int(bounce_y)), 30)
    
    return alpha > 0

def main():
    global ball_x, ball_y, ball_vel_y, ball_vel_x, gravity, max_bounce_height
    global bounce_count, simulation_time, is_dragging, drag_start_x, drag_start_y, ball_trail
    global paused, show_opening_screen, opening_screen_time
    
    clock = pygame.time.Clock()
    opening_screen_time = pygame.time.get_ticks()
    
    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_ball()
                elif event.key == pygame.K_UP:
                    gravity = min(gravity + 1.0, max_gravity)
                elif event.key == pygame.K_DOWN:
                    gravity = max(gravity - 1.0, min_gravity)
                elif event.key == pygame.K_SPACE:
                    # Give the ball a random velocity when space is pressed
                    ball_vel_x = (pygame.time.get_ticks() % 10) - 5
                    ball_vel_y = -((pygame.time.get_ticks() % 10) + 5)
                elif event.key == pygame.K_p:
                    # Toggle pause
                    paused = not paused
            
            # Handle mouse click to set initial velocity
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if show_opening_screen:
                    show_opening_screen = False
                    continue
                    
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check if click is on the pause button
                button_rect = pygame.Rect(20, HEIGHT - 85, 100, 30)
                if button_rect.collidepoint(mouse_x, mouse_y):
                    paused = not paused
                    continue
                
                # Check if click is on the ball (and simulation is paused)
                if paused or math.sqrt((mouse_x - ball_x)**2 + (mouse_y - ball_y)**2) <= ball_radius:
                    is_dragging = True
                    drag_start_x, drag_start_y = ball_x, ball_y
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if is_dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Set velocity based on drag distance and direction
                    drag_factor = 0.2  # Adjust for reasonable velocities
                    ball_vel_x = (mouse_x - drag_start_x) * drag_factor
                    ball_vel_y = (mouse_y - drag_start_y) * drag_factor
                    is_dragging = False
            
            # Handle slider drag
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                handle_x = slider_x + (gravity - min_gravity) / (max_gravity - min_gravity) * slider_width
                
                # Check if clicking on slider handle (but not on the ball)
                if ((mouse_x - handle_x)**2 + (mouse_y - slider_y)**2) <= slider_handle_radius**2:
                    if math.sqrt((mouse_x - ball_x)**2 + (mouse_y - ball_y)**2) > ball_radius:
                        pygame.event.set_grab(True)
            
            if event.type == pygame.MOUSEBUTTONUP:
                pygame.event.set_grab(False)
            
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                if pygame.event.get_grab():
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Update gravity based on slider position
                    new_pos = max(min(mouse_x, slider_x + slider_width), slider_x)
                    gravity = min_gravity + (new_pos - slider_x) / slider_width * (max_gravity - min_gravity)
        
        # Draw everything
        screen.fill(BACKGROUND)
        
        # Draw stars in background
        for i in range(70):  # More stars for larger screen
            x = (i * 37) % WIDTH
            y = (i * 23) % (ground_height - 50)
            size = 1 if i % 3 == 0 else 2
            pygame.draw.circle(screen, (200, 200, 255), (x, y), size)
        
        # Draw opening screen if needed
        if show_opening_screen:
            show_opening_screen = draw_opening_screen()
            pygame.display.flip()
            clock.tick(60)
            continue
        
        # Update ball position if not paused
        if not paused and not is_dragging and (abs(ball_vel_x) > 0.01 or abs(ball_vel_y) > 0.01 or ball_y < ground_height - ball_radius):
            # Formula: v = v₀ + g*t
            ball_vel_y += gravity * time_step
            
            # Formula: y = y₀ + v₀*t + 0.5*g*t²
            ball_y += ball_vel_y * time_step + 0.5 * gravity * time_step**2
            
            ball_x += ball_vel_x * time_step
            
            # Add current position to trail (with max length)
            ball_trail.append((ball_x, ball_y))
            if len(ball_trail) > 20:
                ball_trail.pop(0)
            
            # Track maximum bounce height
            current_height = ground_height - ball_y - ball_radius
            if current_height > max_bounce_height:
                max_bounce_height = current_height
            
            # Bounce off walls
            if ball_x - ball_radius < 0:
                ball_x = ball_radius
                ball_vel_x = -ball_vel_x * elasticity
            elif ball_x + ball_radius > WIDTH:
                ball_x = WIDTH - ball_radius
                ball_vel_x = -ball_vel_x * elasticity
            
            # Bounce off ground (with energy loss)
            if ball_y + ball_radius > ground_height:
                ball_y = ground_height - ball_radius
                # Formula: v' = -e*v (energy loss on bounce)
                ball_vel_y = -ball_vel_y * elasticity
                ball_vel_x *= 0.95  # Slight horizontal friction
                bounce_count += 1
            
            # Update simulation time
            simulation_time += time_step
        
        draw_ground()
        draw_ball_trail()
        draw_ball()
        draw_velocity_vector()
        draw_drag_line()
        draw_ui()
        draw_stats()
        draw_pause_button()
        
        # Draw instructions
        instructions = [
            "Click and drag the ball to set initial velocity",
            "Adjust the slider to change gravity",
            "Press R to reset, SPACE for random velocity, P to pause",
        ]
        
        for i, text in enumerate(instructions):
            instruction = font.render(text, True, TEXT_COLOR)
            screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT - 80 - i * 25))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
