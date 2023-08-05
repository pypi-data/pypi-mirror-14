# Python For MegaPi
## How To Use
 * Compile and upload the Firmware to MegaPi ( https://github.com/Makeblock-Official/FirmwareForMegaPi )
 * On your Raspberry Pi, 
 ```
 git clone https://github.com/Makeblock-Official/PythonForMegaPi
 ```
 * Insert the initial code for starting MegaPi first.
```
 from lib.megapi import *
 bot = MegaPi()
 bot.start()
 ```
 * python your code

## Python API
 * Start
 	* **MegaPi**()
 	* **start**()
 	
 * GPIO
 	* **digitalWrite**( pin, level )
 	* **pwmWrite**( pin, pwm )
 	* **digitalRead**( pin, **def** onResult )
 	* **analogRead**( pin, **def** onResult )
 	
 * Motion
	* DC Motor
	  * **dcMotorRun**( port, speed )
	* Servo Motor
	  * **servoRun**( port, angle )
	* Encoder Motor
	  * **encoderMotorRun**( port, speed )
	  * **encoderMotorMove**( port, speed, distance, **def** onFinish )
	  * **encoderMotorMoveTo**( port, speed, position, **def** onFinish )
	* Stepper Motor
	  * **stepperMotorSetting**( port, microsteps, acceleration )
	  * **stepperMotorRun**( port, speed )
	  * **stepperMotorMove**( port, speed, distance, **def** onFinish )
	  * **stepperMotorMoveTo**( port, speed, position, **def** onFinish )
	  
 * Sensors
 	* Ultrasonic Sensor
 	  * **ultrasonicSensorRead** ( port, **def** onResult ) 
 	* LineFollow Sensor
 	  * **lineFollowerRead** ( port, **def** onResult ) 
 	* Light Sensor
 	  * **lightSensorRead** ( port, **def** onResult ) 
 	* Sound Sensor
 	  * **soundSensorRead** ( port, **def** onResult ) 
 	* Temperature Sensor
 	  * **temperatureRead** ( port, **def** onResult ) 
 	* PIR Motion Sensor
 	  * **pirMotionSensorRead** ( port, **def** onResult ) 
 	* Touch Sensor
 	  * **touchSensorRead** ( port, **def** onResult ) 
 	* LimitSwitch
 	  * **limitSwitchRead** ( port, slot, **def** onResult ) 
 	* Humiture Sensor
 	  * **humitureSensorRead** ( port, type, **def** onResult ) 
 	* Gas Sensor
 	  * **gasSensorRead** ( port, **def** onResult )
 	* Flame Sensor
 	  * **flameSensorRead** ( port, **def** onResult ) 
 	* Button
 	  * **buttonRead** ( port, **def** onResult ) 
 	* Potentiometer
 	  * **potentiometerRead** ( port, **def** onResult )
 	* Joystick
 	  * **joystickRead** ( port, axis, **def** onResult )
 	* 3-Axis Accelerometer and Gyro Sensor
 	  * **gyroRead** ( axis, **def** onResult )
 	* Compass
 	  * **compassRead** ( **def** onResult )
 	
 * Display
 	* RGB Led
 	  * **rgbLedSetColor** ( port, slot, index, r, g, b )
 	  * **rgbLedShow** ( port, slot )
 	  * **rgbLedDisplay** ( port, slot, index, r, g, b )
 	* 7-segment Display
 	  * **sevenSegmentDisplay** ( port, value )
 	* Led Matrix Display
 	  * **ledMatrixDisplayMessage** ( port, x, y, msg )
 	  * **ledMatrixDisplayRaw** ( port, buffer )
 	* Serial LCD Display
 	  * **lcdDisplay** ( string )
 	  
 * Others
 	* DSLR Shutter
	  * **shutterOn** ( port )
	  * **shutterOff** ( port )
	  * **focusOn** ( port )
	  * **focusOff** ( port )
