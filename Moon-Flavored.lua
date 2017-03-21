--Conversion of python breakout to lua for Love2D

WIDTH = 600
HEIGHT = 400
PAD_WIDTH = 80
PAD_HEIGHT = 4
paddle_pos = WIDTH/2
paddle_vel = 0
level = 1
lives = 3
img_bbrick = love.graphics.newImage("waterbrick.png")
img_cbrick = love.graphics.newImage("waterbrick2.png")
img_pbrick = love.graphics.newImage("waterbrick3.png")
img_bubble = love.graphics.newImage("bubble15.png")
img_gbg = love.graphics.newImage("gradientbg.png")
img_splash = love.graphics.newImage("splashtext.png")
img_win = love.graphics.newImage("wintext.png")
sfx_pop = love.audio.newSource("pop.wav", "static")
sfx_level = love.audio.newSource("transition.wav")
levels = {
  {rows = 0, cols = 0, brickgoals = 0, bricktype = img_bbrick},
  {rows = 3, cols = 12, brickgoals = 3*12, bricktype = img_bbrick},
  {rows = 5, cols = 8, brickgoals = 5*8, bricktype = img_cbrick},
  {rows = 4, cols = 10, brickgoals = 4*10, bricktype = img_pbrick},
  {rows = 0, cols = 0, brickgoals = 0, bricktype = img_bbrick},
}
bricklist = {}

ball = { posx = WIDTH/2
       , posy = HEIGHT
       , velx = 0
       , vely = 0
       , launched = false
       , radius = 6
       }
particles = {}

function particles:draw()
  for i, p in ipairs(particles) do
    if p.there then
      love.graphics.draw(img_bubble, p.x, p.y, 0, p.scale, p.scale)
    end
  end
end

function particles:update()
  for i, p in ipairs(particles) do
    p.x = p.x + p.velx
    p.y = p.y + p.vely
    if p.x > WIDTH or p.x < 0 then
      p.there = false
    end
    if p.y > HEIGHT or p.y < 0 then
      p.there = false
    end
  end
end

math.randomseed(os.time())

function particles:add(x, y)
  local nump = math.random(4)
  for i = 1, nump do
    table.insert(self, {x = x, y = y, velx = math.random(7)-2.5, vely = math.random(4)*-1, scale = 1, there = true})
  end
end

function initlist()
  local output = {}
  for row = 1, levels[level].rows do 
    table.insert(output, {})
    for i = 1, levels[level].cols do
      table.insert(output[row], false)
    end
  end
  return output
end

function over(cols)
  return (.5 * (WIDTH-(50*cols)))
end

function build_bricklist(list)
  local xloc, yloc = 0, 0
  for i, rows in ipairs(list) do
    yloc = 25*(i-1)
    xloc = 0
    for j, brick in ipairs(list[i]) do
      table.insert(bricklist, {hit = false, x = xloc+over(#list[i]), y = yloc, sprite = levels[level].bricktype})
      xloc = xloc + 50
    end
  end
end

function check_done()
  for i, brick in pairs(bricklist) do
    if brick.hit == false then
      return false
    end
  end
  return true
end

function level_update()
  reset()
  level = level + 1
  bricklist = {}
  build_bricklist(initlist())
  love.audio.play(sfx_level)
end

function clicked(mx, my, x, y, w, h)
  if mx > x and 
     mx < x+w and 
     my > y and 
     my < y+h
  then return true
  else return false
  end
end

function love.mousepressed(mx, my, button)
  if level == 1 then
    level_update()
    return
  end
  if level == 5 then
    level = 0
    level_update()
    return
  end
  if ball.launched then return
  else
    local x, y = mx - 300, my - 400
    local dist = math.sqrt(x^2 + y^2)
    ball.velx = x/(dist/4)
    ball.vely = y/(dist/4)
    ball.launched = true
  end
  
end

function love.keypressed(key)
  if key == "left" then
    paddle_vel = -4
  elseif key == "right" then
    paddle_vel = 4
  end
  
  if key == "l" then --debug
    for i, brick in pairs(bricklist) do
      brick.hit = true
    end
    if check_done() then
      level_update()
    end
  end
end

function love.keyreleased(key)
  paddle_vel = 0
end

function ball:reset_ball()
  self.posx = WIDTH/2
  self.posy = HEIGHT
  self.velx = 0
  self.vely = 0
  self.launched = false
end

function reset()
  ball:reset_ball()
  paddle_vel = 0
end

function love.load()
  love.window.setMode(WIDTH, HEIGHT) 
  build_bricklist(initlist())
end
   
function love.draw()
  love.graphics.draw(img_gbg, 0, 0)
  if level == 1 then
    love.graphics.draw(img_splash, 0, 0)
    return
  elseif level == 5 then
    love.graphics.draw(img_win, (WIDTH/2 - 272/2), (HEIGHT/2 - 112/2))
    return
  end
  
  for i, brick in pairs(bricklist) do
    if brick.hit == false then
      love.graphics.draw(brick.sprite, brick.x, brick.y)
      if clicked(ball.posx, ball.posy, brick.x, brick.y, 50, 25) then
        brick.hit = true
        particles:add(brick.x+25, brick.y+20)
        ball.vely = ball.vely * -1
        ball.radius = 12
        love.audio.play(sfx_pop)
        if check_done() then
          level_update()
          return
        end
      end
    end
  end
  
  particles:draw()
  
  love.graphics.rectangle("fill", paddle_pos-PAD_WIDTH/2, HEIGHT-PAD_HEIGHT, PAD_WIDTH, PAD_HEIGHT)
  love.graphics.circle("fill", ball.posx, ball.posy, ball.radius)
  
end

function ball:update_ball()
  --handle edge-of-canvas bounces
  if self.posy < 1 then
    self.vely = self.vely * -1
  end
  if self.posx < 1 then
    self.velx = self.velx * -1
  end
  if self.posx > 599 then
    self.velx = self.velx * -1
  end
  
  --update self
  self.posx = self.posx + self.velx*1.5
  self.posy = self.posy + self.vely*1.5
  if self.radius > 6 then
    self.radius = self.radius - 0.5
  end
end

function love.update(dt)
  particles:update()
  ball:update_ball()
  
  --update paddle
  if paddle_pos < (PAD_WIDTH/2) and paddle_vel < 0 then
    paddle_vel = 0
  end
  if paddle_pos > (WIDTH - PAD_WIDTH/2) and paddle_vel > 0 then
    paddle_vel = 0
  end
  paddle_pos = paddle_pos + paddle_vel*2
  
  
  --determine whether paddle and ball collide
  if ball.vely > 0 and ball.posy > 394 and ball.launched then
    if ball.posx < (paddle_pos - PAD_WIDTH/2) or ball.posx > (paddle_pos + PAD_WIDTH/2) then
      ball.launched = false
      lives = lives - 1
      if lives <= 0 then
        --end game, new game
      else
        reset()
      end
    else
      ball.vely = ball.vely * -1
    end
  end   
end
