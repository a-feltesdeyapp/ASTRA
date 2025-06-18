GTK.disable_controller_config

def tick(args)
  setup_circle_render_target(args) if args.state.tick_count == 0
  setup_game(args) if args.state.tick_count == 0
  handle_input(args)
  if args.state.remaining_time == 0
    display_game_over(args)
    restart_game(args) if args.inputs.keyboard.key_down.r
  elsif args.state.paused
    display_pause_screen(args)
  else
    update_timer(args)
    run_game(args)
  end
end

def setup_game(args)
  args.state.user_circle = { x: 640, y: 360, radius: 20 } unless args.state.user_circle
  args.state.target_radius = 50
  args.state.target_positions = [
    { x: 100, y: 100 }, { x: 1180, y: 100 }, { x: 100, y: 620 }, { x: 1180, y: 620 },
    { x: 640, y: 100 }, { x: 640, y: 620 }, { x: 100, y: 360 }, { x: 1180, y: 360 }
  ]
  args.state.active_target_index ||= rand(8)
  args.state.score ||= 0
  args.state.start_time ||= args.state.tick_count
  args.state.time_limit = 120 * 60
  args.state.target_start_time = args.state.tick_count
  args.state.paused ||= false
end

def handle_input(args)
  if args.inputs.keyboard.key_down.p
    args.state.paused = !args.state.paused
    if args.state.paused
      args.state.pause_start_time = args.state.tick_count
    else
      args.state.start_time += args.state.tick_count - args.state.pause_start_time
    end
  end
  restart_game(args) if args.inputs.keyboard.key_down.r
end

def update_timer(args)
  return if args.state.paused
  remaining_ticks = args.state.time_limit - (args.state.tick_count - args.state.start_time)
  args.state.remaining_time = [remaining_ticks / 60, 0].max
end

def run_game(args)
  move_user_circle(args)
  check_for_target_hit(args)
  draw_elements(args)
end

def move_user_circle(args)
  move_speed = 5
  if args.inputs.keyboard.left || args.inputs.keyboard.key_held.a
    args.state.user_circle[:x] -= move_speed
  elsif args.inputs.keyboard.right || args.inputs.keyboard.key_held.d
    args.state.user_circle[:x] += move_speed
  end
  if args.inputs.keyboard.down || args.inputs.keyboard.key_held.s
    args.state.user_circle[:y] -= move_speed
  elsif args.inputs.keyboard.up || args.inputs.keyboard.key_held.w
    args.state.user_circle[:y] += move_speed
  end
  args.state.user_circle[:x] = args.state.user_circle[:x].clamp(args.state.user_circle[:radius], 1280 - args.state.user_circle[:radius])
  args.state.user_circle[:y] = args.state.user_circle[:y].clamp(args.state.user_circle[:radius], 720 - args.state.user_circle[:radius])
end

def check_for_target_hit(args)
  active_target = args.state.target_positions[args.state.active_target_index]

  if args.geometry.point_inside_circle?(args.state.user_circle, active_target, args.state.target_radius)
    distance_to_center = Math.sqrt((args.state.user_circle[:x] - active_target[:x])**2 + (args.state.user_circle[:y] - active_target[:y])**2)
    proximity_score = ((args.state.target_radius - distance_to_center) / args.state.target_radius * 100).to_i
    time_taken = (args.state.tick_count - args.state.target_start_time) / 60.0
    time_bonus = [100 - time_taken.to_i * 10, 0].max
    total_score = proximity_score + time_bonus
    args.state.score += total_score
    args.state.active_target_index = (args.state.active_target_index + 1) % 8
    args.state.target_start_time = args.state.tick_count
  end

end

def draw_elements(args)
  # Draw target circles FIRST (so user sprite can go on top)
  args.state.target_positions.each_with_index do |pos, index|
    color = (index == args.state.active_target_index) ? :green_circle : :red_circle
    args.outputs.sprites << {
      x: pos[:x] - args.state.target_radius,
      y: pos[:y] - args.state.target_radius,
      w: args.state.target_radius * 2,
      h: args.state.target_radius * 2,
      path: color
    }
  end
  # Draw user sprite LAST so it appears on top
  args.outputs.sprites << {
    x: args.state.user_circle[:x] - args.state.user_circle[:radius],
    y: args.state.user_circle[:y] - args.state.user_circle[:radius],
    w: args.state.user_circle[:radius] * 4,
    h: args.state.user_circle[:radius] * 4,
    path:"sprites/ASTRA_sprite.png"
  }
  # UI
  args.outputs.labels << { x: 640, y: 700, text: "Score: #{args.state.score}", size_px: 30, alignment_enum: 1 }
  minutes = args.state.remaining_time / 60
  seconds = args.state.remaining_time % 60
  args.outputs.labels << {
    x: 1180, y: 700,
    text: format("Time: %02d:%02d", minutes, seconds),
    size_px: 30,
    alignment_enum: 2
  }
  args.outputs.labels << { x: 100, y: 700, text: "Press 'P' to Pause/Resume", size_px: 20 }
  args.outputs.labels << { x: 100, y: 670, text: "Press 'R' to Restart", size_px: 20 }
end

def display_game_over(args)
  args.outputs.labels << { x: 640, y: 400, text: "Game Over", size_px: 50, alignment_enum: 1 }
  args.outputs.labels << { x: 640, y: 350, text: "Final Score: #{args.state.score}", size_px: 30, alignment_enum: 1 }
  args.outputs.labels << { x: 640, y: 300, text: "Press 'R' to Restart", size_px: 25, alignment_enum: 1 }
end

def display_pause_screen(args)
  args.outputs.labels << { x: 640, y: 400, text: "Paused", size_px: 50, alignment_enum: 1 }
  args.outputs.labels << { x: 640, y: 350, text: "Press 'P' to Resume", size_px: 25, alignment_enum: 1 }
  args.outputs.labels << { x: 640, y: 300, text: "Press 'R' to Restart", size_px: 25, alignment_enum: 1 }
end

def restart_game(args)
  args.state.user_circle = nil
  args.state.active_target_index = nil
  args.state.score = nil
  args.state.start_time = nil
  args.state.remaining_time = nil
  args.state.paused = false
  setup_game(args)
end

def setup_circle_render_target(args)
  create_circle_render_target(args, :green_circle, [0, 255, 0])
  create_circle_render_target(args, :red_circle, [255, 0, 0])
end

def create_circle_render_target(args, target_name, color)
  radius = 50
  args.render_target(target_name).width = radius * 2
  args.render_target(target_name).height = radius * 2
  args.render_target(target_name).lines.clear
  (0...radius * 2).each do |i|
    h = i - radius
    l = Math.sqrt(radius * radius - h * h) rescue 0
    args.render_target(target_name).lines << [i, radius - l, i, radius + l, *color]
  end
end

def circle_overlap(circle1, circle2, target_radius)
  dx = circle1[:x] - circle2[:x]
  dy = circle1[:y] - circle2[:y]
  distance = Math.sqrt(dx * dx + dy * dy)
  max_distance = circle1[:radius] + target_radius
  return 0 if distance > max_distance
  (max_distance - distance) / max_distance
end
