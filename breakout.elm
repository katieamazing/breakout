module Breakout exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onClick)

import Keyboard
import Time exposing (Time)
import AnimationFrame exposing (..)

import Color
import Element
import Collage

type alias Ball =
  { x : Float
  , y : Float
  , vx : Float
  , vy: Float
  }

type alias Paddle =
  { x : Float
  , vx: Float
  , pwidth : Float
  , pheight : Float
  }

type alias Model =
  { bricks : List (List Bool)
  , ball : Ball
  , paddle : Paddle
  , h : Float
  , w: Float
  }

type Msg = Start
         | KeyDown Keyboard.KeyCode
         | KeyUp Keyboard.KeyCode
         | Frame Time

initialModel : Model
initialModel =
  { bricks = [ [True, False, True], [False, True, True] ]
  , ball = { x = 20, y = 20, vx = 0.1, vy = 0.1 }
  , paddle = { x = 60, vx = 0, pwidth = 80, pheight = 4 }
  , h = 400
  , w = 600
  }

moveBall : Model -> Float -> Ball
moveBall model dt =
  let ball = model.ball in
    if (ball.x < -299) || (ball.x > 299) then
      { ball | x = ball.x + ball.vx*dt*(-1), y = ball.y + ball.vy*dt, vx = ball.vx*(-1) }
    else if ball.y > 199 then
      { ball | x = ball.x + ball.vx*dt, y = ball.y + ball.vy*dt*(-1), vy = ball.vy*(-1) }
    else if ball.y < -199 then
      checkPaddleCollision ball model.paddle dt
    else
      { ball | x = ball.x + ball.vx*dt, y = ball.y + ball.vy*dt }

checkPaddleCollision : Ball -> Paddle -> Float -> Ball
checkPaddleCollision ball paddle dt =
  if (ball.x > paddle.x + (paddle.pwidth/2)) || (ball.x < paddle.x-(paddle.pwidth/2)) then
    --you lose a point, the ball resets
    { x = 20, y = 20, vx = 0.1, vy = 0.1 }
  else
    { ball | x = ball.x + ball.vx*dt, y = ball.y + ball.vy*dt*(-1), vy = ball.vy*(-1) }


updatePaddle : Paddle -> Keyboard.KeyCode -> Paddle
updatePaddle paddle key =
  case key of
    37 ->
      { paddle | vx = limitPaddle (paddle.vx - 0.1) -10 10 }
    39 ->
      { paddle | vx = limitPaddle (paddle.vx + 0.1) -10 10 }
    _ ->
      paddle

limitPaddle : Float -> Float -> Float -> Float
limitPaddle vel lower upper =
  if vel < lower then
    lower
  else if vel > upper then
    upper
  else
    vel


movePaddle: Paddle -> Float -> Paddle
movePaddle paddle dt =
  if paddle.x < -260 then
    { paddle | x = -260, vx = 0 }
  else if paddle.x > 260 then
    { paddle | x = 260, vx = 0 }
  else
    { paddle | x = paddle.x + paddle.vx*dt }

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    Start ->
      ( model, Cmd.none )
    Frame dt ->
      ( { model |
          ball = moveBall model dt,
          paddle = movePaddle model.paddle dt }, Cmd.none )
    KeyDown key ->
      ( { model | paddle = updatePaddle model.paddle key }, Cmd.none )
    KeyUp key ->
      ( model, Cmd.none )

viewRow : List Bool -> Float -> Float -> List Collage.Form
viewRow row startx starty =
  case row of
    [] -> []
    brick :: rest ->
      if brick then
        (viewRow rest (startx+50) starty) ++ ([ Collage.move (startx, starty) (Collage.toForm ( Element.image 50 25 "waterbrick.png"))])
      else
        viewRow rest (startx+50) starty

viewBricks : List (List Bool) -> Float -> Float -> List Collage.Form
viewBricks rows startx starty =
  case rows of
    [] -> []
    row :: rest -> (viewRow row startx starty) ++ (viewBricks rest startx (starty+25))

viewBall : Ball -> Collage.Form
viewBall ball =
  Collage.move (ball.x, ball.y) (Collage.filled Color.white (Collage.circle 10))



view : Model -> Html Msg
view model =
  (Element.toHtml ( Collage.collage 600 400
    ([ Collage.toForm ( Element.image 600 400 "gradientbg.png")]
      ++ (viewBricks model.bricks -275 100)
      ++ [viewBall model.ball]
      ++ [Collage.move (model.paddle.x, -196) (Collage.filled Color.white (Collage.rect model.paddle.pwidth model.paddle.pheight))])
    )
  )


main : Program Never Model Msg
main =
  Html.program
  { init = ( initialModel, Cmd.none )
  , view = view
  , update = update
  , subscriptions = (\model -> Sub.batch
                    [ Keyboard.downs KeyDown
                    , Keyboard.ups KeyUp
                    , AnimationFrame.diffs Frame
                    ]
  )
  }
