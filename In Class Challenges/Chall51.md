# Elevator Interface

## Data Types

```
ButtonType {
    FLOOR
    DOOR_OPEN
    DOOR_CLOSE
}

ButtonPress {
    type: ButtonType
    floor: int
}

DoorCommand {
    OPEN
    CLOSE
}

DoorResult {
    OPENED
    CLOSED
    OBSTRUCTED
}

Direction {
    UP
    DOWN
    STOP
}
```

## On-Car Computer

### Inputs

```
handle_button_press(button: int) -> ButtonPress
```
Takes the button pressed in the car and returns its type, plus the floor number if it was a floor button.

```
read_position_sensor() -> int
```
Returns the floor the car is currently at.

```
receive_arrival(floor: int)
```
Receives arrival notice from the lift motor computer, then rings the bell and opens the doors.

### Outputs

```
update_display(current_floor: int, dest_floor: int)
```
Shows the current floor and destination floor on the screen inside the car.

```
ring_bell()
```
Rings the bell to alert riders that the car has arrived.

```
actuate_doors(command: DoorCommand) -> DoorResult
```
Opens or closes the doors.  Returns OBSTRUCTED if the door motor resistance passes the safety limit while closing.

```
send_floor_request(floor: int)
```
Sends the requested floor to the lift motor computer.

```
send_current_floor(floor: int)
```
Sends the car's position sensor reading to the lift motor computer.

## Lift Motor Computer

### Inputs

```
receive_floor_request(floor: int)
```
Receives the destination floor from the on-car computer.

```
read_motor_position() -> int
```
Returns the car's floor based on the lift motor's own position tracking.

```
receive_current_floor(floor: int)
```
Receives the car's position sensor reading from the on-car computer, used as a redundant check against the motor's position.

### Outputs

```
set_motor(direction: Direction)
```
Drives the motor up or down, or stops it when the current floor matches the destination.

```
send_arrival(floor: int)
```
Tells the on-car computer the car has arrived, so it can ring the bell and open the doors.

## Assumptions

- Door buttons send reserved values, -1 for open, -2 for close, all other values are floor numbers.
- The instructions only list a screen inside the car, so I'm assuming the on-car computer does not control the screens on each floor.
- Floors are numbered starting at 1, with no basement floors.
- The on-car computer forwards position sensor readings to the lift motor computer.
- Both the lift motor and the car have position sensors.  The lift computer compares the two readings as a redundancy check.
- The lift motor computer handles one request at a time (no queuing of multiple floors).