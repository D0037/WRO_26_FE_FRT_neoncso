# FRT Neoncső
## WRO Future Engineers 2026

---

# Team Information

## Team Details

| Item | Information |
|---|---|
| Team Name | FRT Neoncső |
| Country | Hungary |
| School | Budapest Fazekas Mihály Practising Primary and Secondary School |
| Coach | Sásdi Mariann |

## Team Members

| Role | Name | Age |
|---|---|---:|
| Software, electronics, 3D design | Márton Serényi | 16 |
| 3D design, documentation | Ivan Probojcsevity | 16 |
| Software, hardware | Levente Zempléni | 16 |

---

# Project Overview

This project focuses on designing, building, and programming an autonomous vehicle capable of completing the complex challenges of the WRO Future Engineers category.

Team FRT was driven by the challenge of translating engineering principles and problem-solving into practice, and of building a reliable, predictable system in a competition environment full of uncertain variables. Throughout development we followed a systematic process: brainstorming, research, prototyping, testing, and iteration.

_neoncso_ is a **Raspberry Pi**–based, rear-wheel-drive vehicle with Ackermann steering and encoder-based odometry. Its navigation relies on two complementary sensing layers: an **inertial measurement unit (IMU)** holds the heading through a PID controller, three **VL53L1X ToF sensors** measure the distance to the walls, and a **camera** identifies the red and green traffic markers and the parking zone using OpenCV-based HSV color detection.

The control software is built in a modular Python architecture, with separate state machines for the open and obstacle challenges, and a custom web-based HSV calibration tool that lets us quickly retune the vision system to the venue's changing lighting conditions on site.

Our goal is to create an intelligent vehicle that navigates the course reliably, precisely, and quickly, while keeping every decision it makes engineering-based and justifiable.

## Challenge Summary

### 1. Open Challenge

**Goal:** Drive an autonomous car around the track for **3 complete laps** as quickly and accurately as possible. 

Key points:

* No traffic-sign obstacles are placed on the track.
* The track layout changes between rounds because the inner walls can be arranged differently.
* The starting position and driving direction (clockwise or counterclockwise) are randomized.
* The vehicle must:

  * Follow the correct driving direction.
  * Complete 3 laps.
  * Stop in the designated finish section. 
What is tested:

* Lane following
* Cornering accuracy
* Speed and consistency
* Adaptation to changing track layouts

---

### 2. Obstacle Challenge

**Goal:** Complete the same **3 autonomous laps**, but now obey traffic signs and finish with a parking maneuver. 

Additional elements:

* **Red pillar:** pass it on the **right** side.
* **Green pillar:** pass it on the **left** side.
* Traffic signs are placed randomly before each round.
* After finishing the 3 laps, the vehicle must locate the parking area and perform **parallel parking**. 

Scoring rewards:

* Completing laps.
* Not moving traffic signs.
* Starting from the parking lot (optional bonus).
* Successfully parking fully inside the parking area and parallel to the wall. 

What is tested:

* Traffic-sign recognition and decision making.
* Path planning around obstacles.
* Precision vehicle control.
* Autonomous parking.

#### In one sentence

* **Open Challenge:** “Drive 3 laps on a changing track.”
* **Obstacle Challenge:** “Drive 3 laps while obeying red/green traffic signs, then parallel park.”

## Design Philosophy


Our main goal was to make the robot as **size-efficient** as possible. This meant designing the robot to be compact, while still keeping all important functions, such as steering, driving, sensing, and computing, fully usable and reliable.

We chose a smaller design because we realized that several factors are difficult to control perfectly during movement. These include wheel slipping, small inaccuracies in sensor readings, mechanical play in the steering system, and minor errors in motor movement. In a larger robot, these small errors can have a bigger effect on navigation, because the robot needs more space to turn, correct its path, or avoid obstacles.

By making the robot smaller, we increased its tolerance for navigation errors. A compact robot can fit through tighter spaces, make sharper turns, and recover more easily from small positioning mistakes. For example, if the robot slightly misjudges its position or direction, the error is less likely to cause a collision or a major path deviation because the robot takes up less physical space.

This approach also helped reduce the effect of uncontrolled external factors. Wheel slip, for example, can slightly change the robot’s real position compared to what the software expects. Sensor inaccuracies can also cause the robot to detect lines, walls, or objects a little earlier or later than ideal. With a smaller chassis, these small differences are less likely to become serious problems, because the robot has more usable space around it during navigation.

However, making the robot smaller also created new design challenges. All components had to be arranged very carefully, and there was less room for wiring, mounts, gears, sensors, and the onboard computer. Because of this, our design had to balance compactness with functionality. We did not want to make the robot small at the cost of reliability, so every component had to be placed in a logical and space-efficient way.

Overall, our main design philosophy was to create a robot that is compact, precise, and forgiving. By reducing the size of the robot, we made it easier to navigate in uncertain conditions, while still keeping the mechanical and electronic systems strong enough to perform reliably.

---

# Mechanical Design

| Measurement | Value | Unit |
| ----------- | ----- | ---- |
| Height      |   105 | mm   |
| Length      |   145 | mm   |
| Width       |   150 | mm   |
| Weight      |   448 | g    |

Our main design goal was to make the robot as compact as possible while compromising as little as possible on functionality, stability, and reliability. This meant that every part of the robot had to be designed with a clear purpose. Instead of simply making the robot smaller, we focused on using the available space efficiently, so the drivetrain, steering system, sensors, and onboard computer could all fit together without interfering with each other.

A smaller robot has several advantages: it is lighter, easier to maneuver, and can react faster in tight spaces. However, making the robot small also creates challenges. Components become harder to mount, wiring becomes more cramped, and mechanical tolerances become much more important. Because of this, the design process required many iterations and careful planning.

## Chassis

For the chassis, we wanted to create something different from a standard flat plate design. Instead of using a large base plate, we built the structure around two parallel metal rods. These rods act as the main frame of the robot and provide a strong, lightweight foundation for the rest of the components.

The main advantage of this design is modularity. Since the rods run through the robot, different components can be mounted onto them using custom-designed brackets. This makes the robot easier to modify, repair, and improve. If a part needs to be moved or redesigned, we do not need to rebuild the entire chassis; we can simply change the mounting piece.

The rods also help keep the robot rigid. A rigid chassis is important because any bending or twisting can affect steering accuracy, gear alignment, and sensor readings. By using metal rods as the main structural element, the robot can stay strong while still remaining compact.

## Mounting

The mounting system was one of the most important parts of the mechanical design. Since the chassis is based on two parallel rods, every major component needed a specialized mount. These mounts had to hold the parts securely while also keeping them in the correct position relative to each other.

We first designed the steering system because it determines the position of the front wheels and takes up a fixed amount of space. At the same time, we considered the size of the onboard computer, the Raspberry Pi. These two parts — the steering system and the Raspberry Pi — helped determine the distance between the two metal rods.

After this, we started designing the drivetrain. This was more difficult because the motor, gears, differential, driveshaft, and rear wheels all had to line up correctly. Even a small misalignment could cause friction, poor power transfer, or gear skipping.

In the final version, we created separate sensor mounts and a combined mount for the Raspberry Pi. The sensor mounts are designed to keep the sensors stable and pointed in the correct direction. This is important because inaccurate sensor positioning can lead to unreliable data and poor robot behavior. The Raspberry Pi mount was designed to keep the computer secure while still allowing access to ports and cables.

## Steering System

The robot uses an Ackermann steering system. This is the same basic steering principle used in many cars. The main idea behind Ackermann steering is that the two front wheels do not turn at the same angle during a corner.

When a vehicle turns, the inner wheel follows a smaller circle than the outer wheel. Because of this, the inner wheel needs to turn more sharply, while the outer wheel turns at a smaller angle. If both wheels turned at the same angle, one or both wheels would slide sideways instead of rolling smoothly.

Ackermann steering reduces this slipping by making the wheel angles match the natural turning path of the robot. This improves control, reduces energy loss, and makes turning smoother. It is especially useful in tight turns, where the difference between the inner and outer wheel paths becomes more noticeable.

We chose Ackermann steering because it gives the robot more predictable movement. Instead of relying on wheel slipping or skid steering, the robot can turn in a more controlled and efficient way. This also reduces stress on the drivetrain and makes the robot easier to control through software.

## Drivetrain

The drivetrain is responsible for transferring power from the motor to the wheels. Our robot is rear-wheel driven and front-wheel steered. This means the rear wheels push the robot forward, while the front wheels control the direction.

We designed a custom drivetrain based on our previous experience with similar systems. The drivetrain uses a motor, a differential gearset taken from an RC car, custom-designed gears, and a main driveshaft system.

The motor provides rotational motion, but the raw output of the motor is not always directly suitable for driving the wheels. Motors usually spin very fast but may not produce enough torque on their own. Because of this, gears are needed to adjust the balance between speed and torque.

A gear ratio describes how much the gears change the motor’s output. A higher gear reduction increases torque but reduces speed. A lower gear reduction keeps more speed but provides less torque. Finding the correct gear ratio was important because the robot needed enough torque to move reliably, but still enough speed to perform well.

Our final gear ratio is approximately 1:6, using a three-gear reduction. At first, we tested a 1:1.5 reduction, but our torque calculations were too optimistic and the motor could not start the robot reliably without a small push. Because of this, we redesigned the drivetrain with a stronger reduction. This increased usable torque at the wheels and also reduced the top speed, which made it easier to brake before corners and control the robot more accurately. 

Our exact torque numbers are:

Motor wattage = Voltage * Amperage

Torque = Wattage/(2πF) =

Voltage = 6.4V

Amperage =

F = base rpm*(voltage/recomended voltage)=20500*(6.4/12)=10933 rpm

Torque at the wheels = torque*6

## Design Iterations

During the design process, we encountered many problems that required multiple iterations. Our first focus was the driving mechanism. At the beginning, the basic concept worked, but once we started designing the custom differential gearbox holder, most of the mechanical problems appeared.

One of the biggest challenges was that the motor was slightly weaker than we expected. This meant that the first gear setup did not provide enough torque for reliable movement. To solve this, we had to redesign the gear system and adjust the gear ratio. This helped the motor produce more usable force at the wheels.

Another major challenge was part fit. Since many of the components were 3D printed, small measurement errors could cause big problems. In some cases, a difference of only one or two millimeters decided whether the parts fit together or not. Gear spacing, screw holes, rod mounts, and shaft positions all had to be adjusted multiple times.

This taught us that mechanical design is not only about the main idea, but also about the small details. A design can look correct in CAD, but after printing and assembly, problems can still appear. Parts may be too tight, too loose, misaligned, or difficult to assemble.

Through these iterations, we learned the importance of testing and improving the design step by step. Each version helped us understand the robot better. For example, we learned how important gear ratios are in a drivetrain. The gear train must give the motor enough torque to move the robot, but it must also keep enough rotational speed so the robot does not become too slow.

We also learned that compact design requires careful planning. When many components are placed close together, changing one part often affects several others. This meant that the steering, drivetrain, chassis, and electronics could not be designed separately. They had to be developed as one connected system.

---

# Electronics

## Component List

| Component                           | Purpose       | Connection                 | Voltage               | Why we chose it                    |
| ----------------------------------- | ------------- | -------------------------- | --------------------- | ---------------------------------- |
| Raspberry Pi 4                      | Main computer | Camera, I2C, motor control | 5V                    | Enough processing power for OpenCV |
| Pi Camera 3 Wide                    | Vision        | CSI camera port            | Pi powered            | Wide field of view                 |
| MPU6050                             | IMU / gyro    | I2C                        | 3.3V/5V module        | Heading correction                 |
| TOF400C / VL53L1X                   | Wall distance | I2C                        | 3.3V/5V               | Fast short-range distance          |
| SG92R-180 servo                     | Steering      | GPIO/PWM                   | 5V                    | Easy to use                        |
| rp385-st/2270/dv motor with encoder | Driveshaft    | GPIO/PWM                   | battery voltage       | Easily accesible, powerful         |
| 3436343 Amewi battery pack          | Power source  | power input                | 7.4V                  | Portable power                     |


| Name / Part number | Component type                                  |
| ------------------ | ----------------------------------------------- |
| GY-521             | MPU6050 accelerometer + gyroscope sensor module |
| MBRS540T3G         | Schottky diode                                  |
| SPH-2x20P          | 2×20 pin header / connector                     |
| TPS54332DDAR       | Step-down / buck voltage regulator IC           |
| SMD0603-220R-1%    | 220 Ω SMD resistor, 0603                        |
| SMD0603-330R-5%    | 330 Ω SMD resistor, 0603                        |
| SMD0603-1K-5%      | 1 kΩ SMD resistor, 0603                         |
| SMD0603-4.7K-1%    | 4.7 kΩ SMD resistor, 0603                       |
| SMD0603-10K-1%     | 10 kΩ SMD resistor, 0603                        |
| SMD0603-20K-5%     | 20 kΩ SMD resistor, 0603                        |
| SMD0603-100K-1%    | 100 kΩ SMD resistor, 0603                       |
| GRM21BR60J226ME39K | 22 µF ceramic SMD capacitor                     |
| SMD0603-6.8K-5%    | 6.8 kΩ SMD resistor, 0603                       |
| SMD0603-15K-5%     | 15 kΩ SMD resistor, 0603                        |
| SMD0603-47R-1%     | 47 Ω SMD resistor, 0603                         |
| KPT-3216EC         | SMD LED, likely red/orange                      |
| KP-3216 SGD        | SMD LED, likely green                           |
| SMD0603-2.2K-1%    | 2.2 kΩ SMD resistor, 0603                       |
| HPI0630-2R2        | 2.2 µH power inductor                           |
| A4950ELJTR-T       | DC motor driver IC                              |
| 100 uF / 16V       | Electrolytic or SMD capacitor                   |
| GCM1885C2A221FA16J | 220 pF ceramic SMD capacitor                    |
| SMD1206-0.22R-5%   | 0.22 Ω current-sense / shunt resistor, 1206     |
| SMD0603-62K-1%     | 62 kΩ SMD resistor, 0603                        |
| M 2,5 x 6 DF       | M2.5 screw                                      |
| M 3 x 12 HBKNY     | M3 screw                                        |
| M 3 HTL            | M3 threaded insert / spacer / hardware part     |
| M 3 OA             | M3 washer / nut / hardware part                 |
| RC-40-10/FF        | 40-pin female-female ribbon cable, 10 cm        |
| RC-40-20/FF        | 40-pin female-female ribbon cable, 20 cm        |
| PD-QC-AFC-5-20     | USB-C PD / QC / AFC trigger or power module     |
| TACT-65R-F         | Tactile push button                             |
| ST 1/BK (MRS-1)    | Black terminal / connector                      |
| XT30U-M            | XT30 male power connector                       |
| XT30U-F            | XT30 female power connector                     |

## Wiring Diagram

Included in the `schemes/` folder of the repository.

---

## Communication Architecture

The robot uses several communication methods for different parts of the system. These communication methods are important because the robot has to connect sensors, the onboard computer, and development tools in a reliable way.

The main hardware communication protocol used inside the robot is **I²C**. For development and debugging, we used **SSH** to access the Raspberry Pi remotely, and an **HTTP server** for camera and video testing.

---

### I²C Communication

I²C is used for communication between the Raspberry Pi and several sensors.

In our system, I²C is used for sensors such as the gyroscope and the ToF distance sensors. Each device on the I²C bus has its own address, so the Raspberry Pi can request data from the correct sensor.

The main benefit of I²C is that it reduces wiring complexity. Instead of needing separate communication wires for every sensor, several devices can share the same bus. This helped us keep the electronics cleaner and more space-efficient.

---

### SSH for Development and Code Upload

This was useful because we did not need to connect a monitor, keyboard, and mouse to the robot every time we wanted to change the code. We could upload files, run scripts, read errors, and restart programs directly from our development computer.

SSH made testing faster and more practical. Since the robot could stay assembled while we updated the software, we could quickly change code, test the robot, and then adjust the program again if something did not work correctly.

---

### HTTP Server for Video Testing

For camera testing, we used an **HTTP server** to stream video from the robot. This allowed us to view the camera feed in a browser from another device.

This was especially useful for testing the image recognition system. Since the robot relies on camera data to detect colored lines and objects, we needed to see what the robot was actually seeing. The video stream helped us check whether the camera angle, focus, lighting, and color detection were correct.

The HTTP server was also useful for debugging because it made the camera processing visible in real time. Instead of only reading printed values in the terminal, we could visually confirm if the software was detecting the correct areas.

---

### Overall Communication Design

The communication system was designed to keep the robot practical and easy to develop. I²C handles internal sensor communication, SSH handles remote development, and the HTTP server supports camera debugging.

Together, these systems made the robot easier to build, test, and improve. I²C reduced wiring complexity, SSH made code updates faster, and the HTTP video stream helped us understand and tune the camera-based parts of the software.

---

# Sensors

We chose our sensors based on three main priorities: simplicity, reliability, and the ability to combine different kinds of data. Instead of depending on only one sensor type, we wanted the robot to collect information from several independent sources. This is important because every sensor has weaknesses, and no measurement is perfectly accurate in real-world conditions.

Our robot estimates its position and movement using multiple datasets: distance from the walls, color markings on the floor, motor rotation data, steering angle, and readings from the gyroscope and accelerometer. By combining these different measurements, we can reduce the effect of individual sensor errors. This approach is often called sensor fusion, which means using multiple sensor inputs together to create a more accurate understanding of the robot’s position and movement.

For example, motor rotation data can estimate how far the robot has travelled, but it can become inaccurate if the wheels slip. Distance sensors can measure how far the robot is from the walls, but they may be affected by surface angle or reflections. A camera can recognize floor markings and track features, but lighting conditions can influence image processing. The gyroscope can detect changes in rotation, but it may drift over time. By comparing these different sources, the robot can identify when one measurement is unreliable and correct its behavior using the others.

This gives the robot a much better tolerance for imperfect measurements. If one sensor gives a slightly incorrect value, the system does not immediately lose track of its position. Instead, the robot can cross-check the data with other sensors and make a more stable decision. This makes navigation more reliable, especially in a competition environment where lighting, friction, surface quality, and positioning are never perfectly controlled.

Using different datasets also helps us understand the robot’s movement from different perspectives. The camera gives visual information, the ToF sensor gives distance information, the MPU6050 gives motion and orientation data, and the motor drivers give mechanical movement data. Together, these create a more complete picture of what the robot is doing and where it is on the track.

## Camera System
The robot uses a Pi Camera 3 Wide, which is one of the most important sensors in our system. Its wide field of view allows the robot to see more of its surroundings at once. This is especially useful because the robot can detect lines, floor markings, obstacles, and nearby objects without needing to physically move the camera.

Compared to a standard narrow-angle camera, the wide camera gives better environmental awareness. A narrow camera may provide a more focused image, but it sees a smaller area. For our robot, seeing more of the track is more useful than seeing a small area in extreme detail. The wider view helps the robot react earlier and gives the software more visual information to work with.

The camera is also small and lightweight, which makes it suitable for a compact robot. Since our design focuses heavily on size efficiency, we needed sensors that would not take up too much space or add unnecessary weight.

Another major advantage is that the Pi Camera 3 Wide is designed to work with Raspberry Pi systems. This makes integration easier because it has good software support, low latency, and strong compatibility with the Raspberry Pi 4. Low latency is especially important for real-time vision tasks because the robot needs to react quickly to what it sees.

The camera data is mainly used for visual navigation. It helps us to detect the colored lines on the floor, track the boundaries of the marker blocks. However, camera data can be affected by lighting conditions, shadows, motion blur, and reflections. This is why we do not rely only on the camera. Instead, its data is combined with other sensors to make the robot’s decisions more reliable.

## Gyroscope
We chose the MPU6050 sensor because it is simple, accessible, well-documented, and familiar to us. Since it is widely used in robotics projects, there are many examples, libraries, and resources available. This made it easier to integrate into our system and reduced the risk of spending too much time solving basic communication problems.

The MPU6050 includes both a gyroscope and an accelerometer. The gyroscope measures rotational movement, while the accelerometer measures acceleration along different axes. Because the sensor can measure motion in three axes, it can provide useful information about how the robot moves and turns.

The gyroscope is especially useful for detecting changes in direction. For example, when the robot turns, the gyroscope can measure the rotation and help estimate the robot’s heading. This is important because the robot needs to know not only where it is, but also which direction it is facing. The accelerometer measures changes in speed and movement direction. In theory, acceleration data can help estimate movement, but in practice it can be noisy and affected by vibration. Because of this, we use it mainly as supporting data rather than as the only source of position information.

One important concept with this sensor is drift. Drift means that small errors build up over time, causing the measured angle or position to slowly become inaccurate. This is a common issue with gyroscopes. To reduce this problem, we use a custom calibration algorithm. When the robot starts a round, it takes a large sample of gyroscope measurements while standing still, calculates the average offset, and subtracts this offset from later measurements. This gives the program more reliable heading data.

## ToF Sensors

We chose the ToF400C because it is easy to work with, accurate enough for our needs, and simpler than a full LiDAR system. A ToF sensor measures distance by sending out light and measuring how long it takes for the reflection to return. This allows it to estimate how far away an object or wall is. The ToF400C uses light-based measurement, which makes it better suited for compact robotic navigation where quick and accurate distance readings are useful.
Compared to ultrasonic sensors, ToF sensors are often more precise and faster at short distances. Compared to LiDAR, the ToF400C is much simpler. A LiDAR system can provide much more detailed mapping data, but it is also more expensive, more complex, and harder to process. For our robot, we did not need a full 3D or 2D map of the environment. We mainly needed reliable distance readings that could be processed by a simple algorithm.

The ToF400C provides an easily understandable type of data: distance. This makes it practical for decision-making. For example, if the robot knows how far it is from the left or right wall, it can estimate its position inside the track and correct its path if it gets too close to one side.

However, ToF sensors can still have imperfections. Their measurements may be affected by reflective surfaces, dark surfaces, transparent materials, or unusual angles. This is another reason why we combine ToF data with camera, motor, and gyroscope data instead of relying on it alone.

## Additional Sensors

Although the motors are not traditional sensors, their position feedback gives us another important dataset. Because the motor drivers allow us to know the motor position or rotation, we can calculate approximately how far the robot has travelled.

This method is often called odometry. Odometry estimates movement based on wheel rotation. If we know the wheel diameter and how much the motor has rotated, we can calculate the distance travelled in centimeters. This is useful because it gives the robot a continuous estimate of its movement, even when visual or distance data is temporarily unreliable.

By also tracking the steering angle, we can estimate the path the robot has taken. If the robot moves forward while the wheels are turned, it follows a curved path. By combining travelled distance with steering angle, we can create an approximate layout of the robot’s journey. This helps estimate the robot’s position on the track.

However, odometry also has weaknesses. If the wheels slip, the motor may rotate even though the robot does not move the expected distance. Small errors in wheel diameter, gear ratios, or steering angle can also build up over time. Because of this, odometry is useful, but it should not be the only navigation method.

## Power System

The robot is powered by a 7.4V Amewi battery pack, which provides the main energy source for the drive motor and the onboard electronics. Because the Raspberry Pi, sensors, servo, and logic-level electronics require stable low-voltage power, the battery voltage is converted to a regulated 5V supply using a buck converter circuit based on the TPS54332 regulator. This stable 5V rail is important because the Raspberry Pi is sensitive to voltage drops, especially while processing camera data and controlling multiple sensors at the same time.

The drive motor is one of the largest power consumers in the robot, so it is controlled through the motor driver instead of being connected directly to the Raspberry Pi. This protects the controller and allows the software to control motor speed and direction safely. All electronic parts share a common ground, which is necessary so that PWM, GPIO, I²C, and sensor signals have the same voltage reference.

During testing, we found that power stability and thermal stability are closely connected. Long motor and battery tests caused the Raspberry Pi to overheat when the cooling system was removed, so we added a fan and cooling board. This made the robot more reliable during longer runs and reduced the chance of crashes, throttling, or camera connection problems during the challenge.

---

# Software Architecture

## Software Overview

The robot’s software is built as a modular Python-based control system running on the Raspberry Pi. Its purpose is to read sensor data, process camera input, control the drive motor and steering servo, and make real-time navigation decisions during the WRO Future Engineers challenges.

The architecture separates the main challenge logic from the lower-level hardware control modules. This makes the code easier to test, debug, and improve, because sensors, movement, image processing, and logging are each handled in their own files. The main program can therefore focus on decision-making, while the utility modules handle direct communication with the electronic components.

The software is designed around continuous feedback. The robot constantly reads its gyroscope, ToF distance sensors, motor encoder, and camera image. These inputs are used to correct the steering angle, maintain direction, detect walls or obstacles, and follow the correct path during the challenge. Debugging tools such as logging and live video streaming are also included, which helped during testing and calibration.

## Repository Structure

The repository follows the standard WRO engineering documentation structure.

* `src/` contains the robot control software.
* `src/open.py` contains the main program for the open challenge.
* `src/obstacle.py` is reserved for the obstacle challenge logic.
* `src/config.py` stores shared configuration values, GPIO pins, sensor addresses, HSV color filters, thresholds, and tuning constants.
* `src/test.py` contains testing functions for individual subsystems such as ToF sensors, camera processing, encoders, and movement.
* `src/requirements.txt` lists the Python libraries needed to run the software.
* `src/utils/` contains reusable helper modules for hardware and debugging.
* `src/utils/gyro.py` handles gyroscope and accelerometer readings.
* `src/utils/tof.py` handles the VL53L1X time-of-flight distance sensors.
* `src/utils/movement.py` controls the motor, steering servo, and encoder-based movement.
* `src/utils/image_proc.py` handles camera capture and computer vision processing.
* `src/utils/stream.py` provides a Flask-based live camera/debug stream.
* `src/utils/log.py` provides file and console logging.
* `models/` stores 3D-printable or manufacturable model files.
* `schemes/` stores wiring and electronic diagrams.
* `v-photos/` and `t-photos/` store vehicle and team photos.
* `video/` stores the driving demonstration video link.
* `other/` stores extra technical documentation and supporting files.

This structure keeps the engineering documentation and the robot software in one place, while still separating code, models, diagrams, photos, and videos clearly.

## Module Description

### `open.py`

`open.py` is the main control file for the open challenge. It initializes the GPIO system, movement module, ToF sensors, camera module, and gyroscope. After setup, it enters the main driving loop.

Inside the loop, the robot reads distance values from the ToF sensors and heading data from the gyroscope. It calculates the difference between the target heading and the current heading, then uses this error to correct the steering. The steering correction uses proportional and derivative-style feedback so that the robot can keep a stable direction instead of constantly overcorrecting.

The file also includes constants for speed, steering center, steering direction, heading correction, and centering correction. These values can be tuned during testing to make the robot drive more smoothly.

### `config.py`

`config.py` acts as the central configuration file of the robot. It contains values that are used by multiple modules, including GPIO pin numbers, I²C addresses, logging settings, motor encoder conversion factors, ToF timing values, and HSV color filters.

Keeping these values in one file makes calibration easier. For example, if a sensor pin, color threshold, or motor parameter changes, it can be adjusted in `config.py` without rewriting the whole program.

### `utils/gyro.py`

The gyroscope module communicates with the MPU6050 sensor through I²C using SMBus. It reads raw gyroscope and accelerometer values, converts them using scale factors, and calculates the robot’s rotation around the Z axis.

A separate background thread continuously updates the current heading value. At startup, the gyroscope is calibrated by taking many samples and calculating an offset. This reduces drift and improves the accuracy of the heading correction.

The module provides functions for resetting the heading, reading the current angle, reading raw gyroscope values, reading accelerometer values, and safely stopping the background thread.

### `utils/tof.py`

The ToF module manages three VL53L1X distance sensors: front, left, and right. Since these sensors normally share the same default I²C address, the software uses their XSHUT pins to start them one by one and assign separate addresses.

After setup, the module continuously polls the sensors in a background thread. The latest valid distances are stored in a shared dictionary and can be accessed through simple functions such as `get_front()`, `get_left()`, and `get_right()`.

This module is important for wall detection, centering, and obstacle awareness. It allows the main program to quickly access distance data without blocking the rest of the robot’s control loop.

### `utils/movement.py`

The movement module controls the drive motor, steering servo, and motor encoder. It uses Raspberry Pi GPIO pins for motor direction and PWM control, and hardware PWM for the steering servo.

The module provides functions to set the steering angle, set motor speed, read encoder position, estimate speed, and move a given distance. The encoder interrupt callback updates the position counter whenever the encoder signal changes.

The `move()` function also includes a basic PID-style correction system. It uses the gyroscope heading to keep the robot moving straight while travelling a target distance.

### `utils/image_proc.py`

The image processing module handles camera capture using the Raspberry Pi camera. It captures frames in a separate thread, rotates the frame, applies preprocessing, and stores the latest image for use by other parts of the program.

It uses OpenCV and HSV color filtering to detect colored features. The `get_direction()` function detects orange and blue line regions and compares their positions to decide which direction is indicated. The `get_blocks()` function detects red and green blocks by applying HSV filters, contour detection, and area filtering.

The module also removes irrelevant parts of the image using black wall/line masking. This helps reduce noise and makes the vision system focus on the useful part of the camera frame.

### `utils/stream.py`

The stream module provides a live debugging stream using Flask. Other modules can send frames to it with `stream.show(name, frame)`, and the stream server makes these frames viewable over the network.

This is useful during development because the team can see what the robot camera sees and how the processed debug image looks. It makes it much easier to tune HSV filters, check line detection, and understand camera-based errors.

### `utils/log.py`

The logging module writes timestamped messages to both the console and a log file. It supports different log levels such as debug, info, warning, and error.

Logging is useful during testing because it records sensor values, detected events, warnings, and movement behavior. This makes it easier to find problems after a test run and compare different software versions.

### `test.py`

`test.py` contains small test routines for checking individual components. It can be used to test ToF distance readings, image processing, motor encoder readings, and movement behavior.

This file is important because the robot has many connected subsystems. Testing them separately helps identify whether a problem comes from the software, wiring, sensor calibration, or mechanical design.

## Program Flow

The program starts by importing the configuration file and the utility modules. Then it initializes the Raspberry Pi GPIO mode and sets up the hardware systems.

First, the movement module is prepared, including the motor PWM, servo PWM, and encoder input. Next, the ToF sensors are initialized and assigned their separate I²C addresses. The camera system is started in the background, and the gyroscope is calibrated and reset.

After setup, the robot enters its main control loop. In this loop, the robot repeatedly reads the ToF sensors and the gyroscope. The gyroscope gives the current heading, while the ToF sensors provide distance information from the front, left, and right sides.

The software then calculates the heading error by comparing the current heading with the target heading. A steering value is calculated from this error. The proportional part reacts to how far the robot is from the target angle, while the derivative part reacts to how quickly the robot is rotating. This helps the robot correct its direction smoothly.

If side distance data is available, the software also applies a centering correction. This compares the left and right distance sensor values and adjusts the steering so the robot can stay more centered between walls.

Finally, the movement module applies the calculated steering angle and sets the motor speed. This loop continues until the challenge logic decides that the required number of corners or sections has been completed. On interruption or shutdown, the program stops the gyroscope thread, camera thread, motor PWM, servo PWM, and GPIO outputs safely.

## Sensor Processing

The robot uses multiple sensors because no single sensor gives enough information for reliable autonomous driving. Each sensor type has a different role in the software architecture.

The gyroscope is used for heading estimation. It measures angular velocity around the Z axis, and the software integrates this value over time to estimate the robot’s current rotation. Before driving, the gyroscope is calibrated to reduce drift. During movement, the heading value is used for steering correction, allowing the robot to maintain a stable direction even if the floor, motor power, or mechanical friction causes small deviations.

The ToF sensors measure distance to nearby objects and walls. The front sensor is used to detect objects or approaching walls, while the left and right sensors help the robot understand its position inside the track. The software reads these sensors continuously in a background thread, so the main program always has access to the most recent valid distance values. This makes the robot more responsive and prevents sensor reading delays from slowing down the driving loop.

The camera is used for visual detection. The image processing system converts the camera image into HSV color space, which makes it easier to isolate specific colors under changing lighting conditions. HSV filters are used to detect orange, blue, red, and green objects or lines. Morphological operations such as erosion and dilation reduce noise, and contour filtering removes small false detections.

For line direction detection, the software compares the detected position of orange and blue regions. Depending on which color appears lower or more relevant in the frame, the function returns a direction decision. For block detection, red and green masks are processed with contour detection, and the software calculates the center point and area of each detected block.

The motor encoder is used for position feedback. It counts wheel or motor movement through GPIO interrupts, and the software converts encoder ticks into travelled distance using a conversion factor. This makes distance-based movement possible and also allows testing of motor behavior.

All sensor processing is connected through the main control loop. The gyroscope provides orientation, ToF sensors provide distance, the camera provides visual interpretation, and the encoder provides movement feedback. By combining these inputs, the robot can drive more accurately than it could with only one sensor.

---

# Navigation

## Line Following

The robot uses a camera-based navigation system to detect colored lines and visual markers on the field. The Pi Camera captures live video frames, which are processed using OpenCV. The image is converted into HSV color space, because HSV filtering is more reliable for detecting colors under changing lighting conditions than using raw RGB values.

The software contains predefined HSV ranges for orange, blue, red, green, and magenta colors. These thresholds are stored in the configuration file, so they can be tuned without rewriting the full vision algorithm. During processing, the image is filtered by color, and the resulting masks are cleaned with erosion and dilation. This removes small noise and makes the detected line areas more stable.

For line detection, the robot mainly compares orange and blue regions. The image processing module finds the visible colored areas, calculates their average position, and then decides which line is currently dominant. If the orange region appears lower or more relevant in the image than the blue region, the function returns one direction; if the blue region is more dominant, it returns the opposite direction.

This allows the robot to recognize the direction of the track or turn markers. Instead of following a simple black line, the robot uses color-based interpretation to understand which way it should continue. The camera system also includes a preprocessing step that masks out irrelevant parts of the frame above the detected black wall or dark boundary. This helps the algorithm focus on the useful lower part of the image and reduces false detections.

The line-following system is supported by the gyroscope. While the camera gives visual direction information, the gyroscope helps the robot keep a stable heading. This combination makes the navigation more accurate than relying only on the camera, because the robot can still maintain direction even when the camera frame is temporarily unclear.

## Obstacle Detection

Obstacle detection is handled by two main sensor systems: the Time-of-Flight distance sensors and the camera.

The ToF sensors measure the distance between the robot and nearby walls or objects. The robot uses front, left, and right distance readings to understand its surroundings. The front sensor is used to detect objects or walls in front of the robot, while the side sensors help estimate how centered the robot is inside the track.

The ToF module initializes the VL53L1X sensors using their XSHUT pins. Since these sensors normally use the same default I²C address, the software starts them one by one and assigns them separate addresses. After initialization, the sensors are read continuously in a background thread. This means the main driving program can access the most recent distance values without waiting for a slow sensor reading.

The camera also contributes to obstacle detection by identifying colored blocks. The image processing module filters the camera frame for red and green colors, then uses contour detection to locate block-shaped objects. Small contours are removed using an area threshold, so random noise is ignored. For each detected block, the software calculates its center point and visible area.

Red and green blocks are important because they are not just obstacles; they also tell the robot which side to pass on. The block color and position help the software decide the avoidance direction. A larger detected area usually means that the block is closer or more important, while the center position tells whether it is on the left, right, or middle of the camera view.

By combining ToF distance data with camera-based color recognition, the robot can detect both physical distance and visual obstacle type. This gives the navigation system more information than a single sensor could provide.

## Obstacle Avoidance

Obstacle avoidance is based on steering decisions made from sensor feedback. The robot uses Ackermann steering, meaning it behaves more like a real car than a tank-drive robot. Because of this, obstacle avoidance must be smooth and planned; the robot cannot simply rotate in place.

The first layer of avoidance comes from the ToF sensors. If the front distance becomes too small, the robot knows that something is in front of it and must react. The side sensors help decide which side has more free space. If the left side has more distance than the right side, the robot can steer left; if the right side has more distance, it can steer right.

The second layer of avoidance comes from the camera. When the camera detects a red or green block, the robot can use the block’s color and position to choose a passing direction. The detected contour center tells the robot where the obstacle appears in the camera image. The visible area of the contour helps estimate how close or important the obstacle is.

The steering correction is also influenced by the gyroscope. The open challenge code calculates a heading error by comparing the target angle with the current gyro angle. A proportional term reacts to the size of the heading error, while a derivative-style term uses angular velocity to reduce overcorrection. This allows the robot to steer around obstacles while still keeping its movement stable.

Side-distance correction is also used to keep the robot centered. The software compares the left and right ToF values and adds a centering correction to the steering angle. This helps the robot avoid drifting too close to one wall while driving through the track.

The motor and steering are controlled separately. The drive motor sets the forward speed, while the steering servo sets the angle of the wheels. This separation allows the robot to slow down, turn, correct its direction, and then continue forward smoothly after passing an obstacle.

## Recovery Strategies

Recovery strategies are important because real-world robot movement is never perfect. The robot may face unclear camera images, sensor noise, wrong detections, wheel slip, or unexpected contact with walls or obstacles. The software architecture includes several ways to reduce these problems.

The first recovery method is gyro-based heading correction. If the robot starts turning too far away from its intended direction, the gyroscope detects the change in angle. The steering system then applies a correction to return the robot closer to the target heading. This helps the robot recover from small mechanical errors, uneven motor power, or slight impacts.

The second recovery method is ToF-based centering. If the robot gets too close to one side of the track, the side distance sensors detect the imbalance. The steering correction then pushes the robot back toward the center. This is especially useful after turns or obstacle avoidance maneuvers, where the robot may not be perfectly aligned.

The third recovery method is camera noise filtering. The vision system does not directly trust every colored pixel. It uses HSV filtering, erosion, dilation, contour filtering, and area thresholds to remove small false detections. This prevents the robot from reacting to random reflections, shadows, or tiny colored objects that are not relevant to navigation.

The fourth recovery method is continuous sensor updating. The camera, gyroscope, and ToF sensors are updated continuously or in background threads. This means the robot does not depend on a single reading. If one frame or one distance value is wrong, the next readings can correct the decision quickly.

The fifth recovery method is safe cleanup. If the program is interrupted, the software stops the gyro thread, camera thread, motor output, steering output, and GPIO system. This prevents the robot from continuing to drive uncontrollably after a software stop or testing interruption.

Possible future recovery improvements could include a stuck-detection system using the motor encoder, automatic reverse movement when the front ToF sensor detects a very close obstacle, and a “search mode” when no valid line or block is visible for several frames. These additions would make the robot even more reliable during difficult runs.

---

# Control Systems

The robot’s control system is based on sensor feedback. This means the robot does not simply follow fixed movements, but constantly reacts to what the sensors detect.

The most important control inputs are the ToF distance sensors and the camera system. The ToF sensors detect changes in distance from walls or obstacles. If the robot notices that a wall is ending, getting too close, or suddenly changing distance, it can decide to turn, correct its path, or stop.

The camera is the second major decision-making input. It uses color and image recognition to detect track markings and obstacles. This allows the robot to react not only to distances, but also to visual information, such as colored lines or colored blocks.

Using both distance-based and camera-based control makes the robot more reliable. The ToF sensors give simple and fast distance data, while the camera gives more detailed information about the track and objects.

## Steering Control

The steering control is designed to be simple and predictable. During the open challenge, the robot mainly decides when and where to turn based on wall detection and colored line detection.

If a ToF sensor detects that a wall has ended or disappeared, the robot interprets this as a possible corner or turning point. At the same time, the camera checks for colored lines on the track. The robot uses the first detected line and the first wall disappearance to decide whether it should follow a clockwise or counter-clockwise route.

This allows the robot to choose the correct turning direction automatically instead of relying on a fully pre-programmed path.

During the obstacle challenge, steering decisions are mainly based on camera recognition. The camera detects the color and position of obstacles, and the robot uses this information to decide how to steer around them.

Important concepts:

- **ToF-based steering:** the robot uses distance changes to decide when to turn.
- **Camera-based steering:** the robot uses visual information, such as colored lines or blocks, to choose direction.
- **Clockwise and counter-clockwise navigation:** the robot identifies whether it should follow the track by turning mostly right or mostly left.
- **Feedback control:** the steering is adjusted using live sensor data instead of fixed timing.

## Speed Control

The robot mostly uses a constant driving speed while moving. This makes the control system simpler and more predictable, because the robot does not need to constantly calculate different speed levels during normal driving.

During turns, the rear differential helps balance the speed difference between the two rear wheels. This is important because when the robot turns, the outer wheel travels a longer path than the inner wheel. The differential allows the wheels to rotate at different speeds, which reduces slipping and makes turning smoother. The robot also reduces its motor speed during turns.

Even though the speed is mostly constant, the robot can still stop or slow down when needed. For example, if the ToF sensors detect an obstacle or an unexpected wall distance, the control system can react by stopping the robot or preparing for a turn.

Important concepts:

- **Constant speed:** makes movement easier to control and tune.
- **Differential gearset:** allows the rear wheels to rotate at different speeds during turns.
- **Wheel slip reduction:** improves stability and efficiency.
- **Sensor-triggered stopping:** allows the robot to react when an object or wall is too close.
---

# Testing

We performed tests on most major components, including the motors, batteries, drivetrain, cooling system, sensors, and software. Our goal was not only to check whether each part worked, but also to see how it behaved under less ideal conditions.

We also tried to calculate everything that could be calculated before building. This included gear ratios, clearances, expected movement distances, sensor positions, and mechanical tolerances. We followed manufacturer data wherever possible, especially for electronic components, sensors, motors, and batteries.

## Test Methodology

Our testing method was based on two main ideas: testing components separately and then testing them inside the complete system.

First, we tested individual parts to make sure they worked on their own. This made it easier to find problems because we could focus on one component at a time. After that, we tested the same parts again after assembling them into the full robot. This was important because a component can work alone, but still cause problems when placed inside the final system.

We also tried to simulate harsher conditions than normal. These included high temperature, reduced battery voltage, worse lubrication, and traction loss. This helped us check whether the robot could still function if the environment was not ideal.

For example, we tested the motors and batteries in the main hall of our school, where the temperature was around 35°C. We wrote a simple test program that continuously ran the motors until the battery drained. This allowed us to test battery life, motor heating, and general reliability.

We repeated a similar test after the electronics were fully assembled. The first result was not ideal because we had removed the full cooling system from the Raspberry Pi 4. During the test, the Raspberry Pi constantly overheated, so we had to assemble a fan and cooling board for the CPU. After improving the cooling, the system became more reliable.

For 3D-printed parts, we generally used a tolerance of around 0.2 mm. In some cases, this was not enough because printed parts do not always come out exactly as designed. Small errors in printing, material shrinkage, or assembly alignment could cause parts to fit too tightly or too loosely. When this happened, we adjusted the parts manually using grinding and filing, or redesigned the part when needed.

## Mechanical Testing

Mechanical testing focused mainly on the drivetrain, gears, driveshaft, tires, and lubrication. Since several drivetrain parts were 3D printed, we wanted to make sure they could survive longer operation without breaking, slipping, or overheating.

One important test compared two types of lubrication for the driveshaft: WD-40 and lithium grease. The goal was to see which one reduced friction better and helped the drivetrain run more smoothly. In the end, we chose the lithium grease, because it was easier to apply, and it stayed on much longer.

This test was also a durability test for the gears and the 3D-printed driveshaft. At first, we did not fully trust the strength of the printed drivetrain parts, especially under continuous load. However, the system performed much better than expected and survived the test successfully.

We also tested tire slip by putting a small amount of water on the wheels. This simulated a low-traction situation where the wheels could lose grip. The robot was still able to function, but it performed much better under normal dry conditions.

This confirmed that the drivetrain works, but it also showed that traction is very important for accurate navigation. If the wheels slip, the robot may travel less than expected even though the motors are rotating. This can affect odometry and turning accuracy. We try to correct this using sensor feedback, but wheel slip can still create problems. During normal laps, without external effects on the drivetrain, the robot and software perform reliably.

## Sensor Testing

Sensor testing was done to improve the accuracy and reliability of the robot’s measurements. Since our navigation depends heavily on sensor data, even small sensor errors can affect movement decisions.

We tested the accuracy of the ToF sensors under different lighting conditions. They were least accurate in direct sunlight and most stable under indoor LED lighting. During normal tests with known distances, the readings stayed within our acceptable error range, so we did not add additional software correction. To reduce gyroscope drift, we calibrate the gyroscope at every startup.

## Software Testing

Software testing was done by testing each module separately before using it in the full robot program. This helped us find problems faster and made debugging easier.

We tested the motor control code by running the motors at different speeds and checking whether the robot responded correctly. We also tested steering control by sending different steering angles and checking whether the wheels moved to the expected positions.

The sensor modules were tested separately as well. The ToF sensors were checked by printing distance values to the terminal. The gyroscope was tested by rotating the robot and checking whether the measured angle changed correctly. The camera system was tested by checking whether it could detect the correct colors and markings.

We also used logging and camera streaming during testing. Logging helped us review values after a test, while camera streaming allowed us to see what the robot was detecting in real time. This was especially useful for tuning color recognition, because lighting conditions can strongly affect camera-based detection. 

The main goal of software testing was to make sure that each part of the program worked before combining everything. This reduced the chance of hidden errors in the final system.

## System Testing

During system tests, we checked whether the robot could move, steer, read sensors, process camera data, and react correctly at the same time. We encountered several problems related to component communication, torque calculations, steerability, and sensor accuracy. The robot had to be reassembled and adjusted several times, but after multiple test cycles, the systems came together as a working unit.

---

| Test                        | Condition                                 | Result                                                               | Improvement                             |
|-----------------------------|-------------------------------------------|----------------------------------------------------------------------|-----------------------------------------|
| Motor and battery heat test | Motors running continuously in ~35°C hall | Motors and battery survived, Raspberry Pi overheated without cooling | Added fan and cooling board             |
| Lubrication test            | WD-40 vs lithium grease on drivetrain     | Lithium grease stayed longer and reduced friction better             | Used lithium grease                     |
| Tire slip test              | Small amount of water on wheels           | Robot still moved, but odometry became less reliable                 | Use sensor feedback to correct movement |
| ToF lighting test           | Indoor LED lighting vs sunlight           | ToF sensors were more stable indoors                                 | Calibrate under competition lighting    |
| Gyro drift test             | Robot standing still before run           | Drift can build up over time                                         | Gyro offset calibration at startup      |

---

# Development Process

Our development process followed an iterative engineering cycle. Instead of trying to build the final robot in one step, we moved through several stages: planning, designing, building, testing, improving, and retesting. If a problem appeared during testing, we returned to an earlier stage and improved the design before moving forward again.

This process helped us avoid relying on assumptions. Each version of the robot gave us new information, and we used that information to make the next version better.

---

## 0. Brainstorming About Principles

The first step was brainstorming the main design principles of the robot. Before choosing exact parts or designing models, we discussed what the robot needed to achieve and what priorities should guide the whole project.

Our main principles were compact size, reliable movement, simple maintenance, accurate sensing, and strong mechanical stability. We wanted the robot to be as small as possible, but not at the cost of important functionality. This meant every component had to have a clear purpose and a logical position inside the robot.

We also considered which systems would be the most important for the challenges. These included steering, drivetrain efficiency, sensor placement, camera visibility, battery reliability, and software control. By defining these principles early, we had a clearer direction during the rest of the development.

---

## 1. CAD Design, Electronics Design, and Choosing Parts

After defining the main principles, we started designing the robot in CAD. This included both the mechanical 3D design and the layout of the electronic components.

For the mechanical CAD, we designed the chassis, steering system, drivetrain mounts, sensor mounts, Raspberry Pi mount, and other structural parts. The CAD model helped us check whether all components could fit together before printing or assembling anything.

We also planned the electronics layout. This included choosing where to place the Raspberry Pi, motor drivers, sensors, battery, wiring, and cooling system. Electronics placement was important because poor cable routing could cause reliability problems later.

At the same time, we chose the main components. We selected parts based on availability, size, documentation, compatibility, and how easily they could be integrated into our system. We tried to choose parts that were reliable but still simple enough to work with during development.

---

## 2. Checking Every Measurement

Before manufacturing or assembling parts, we checked all important measurements. This included component dimensions, hole spacing, rod distances, shaft positions, gear spacing, sensor angles, cable clearance, and mounting points.

This step was important because small measurement errors can cause major problems in a compact robot. A difference of one or two millimeters can decide whether a part fits, whether gears mesh correctly, or whether a sensor has a clear view.

We compared CAD dimensions with real component measurements whenever possible. Manufacturer datasheets were useful, but we also measured physical parts ourselves because real parts are not always exactly the same as their official drawings.

By checking measurements carefully, we reduced the number of failed prints and assembly problems.

---

## 3. 3D Printing and Assembly

After checking the design, we 3D printed the required parts and started assembly. This stage turned the CAD model into a real physical robot.

During assembly, we tested how well the printed parts fit with the metal rods, motors, gears, sensors, and electronics. Some parts fit correctly immediately, while others needed small adjustments. In some cases, we used filing, grinding, or sanding to make parts fit better. In other cases, we returned to CAD and changed the model.

Assembly also helped reveal problems that were not obvious in CAD. For example, a part might look correct digitally but be difficult to tighten, hard to access, or too close to wires or moving components. Because of this, assembly was not only a building step, but also another form of testing.

---

## 4. Testing and Returning to Step 0 if Necessary

After assembly, we tested the robot and its individual systems. This included mechanical testing, electronics testing, sensor testing, software testing, and full-system testing.

The goal of testing was to find weak points. We checked whether the robot could drive, steer, detect walls, recognize colors, read sensor data, and react correctly. We also tested the drivetrain, battery, cooling, and sensor accuracy.

If a major problem appeared, we returned to an earlier stage of the process. Sometimes this meant changing a CAD part, choosing a different component, changing the electronics layout, or rethinking the original design principle.

This made the process iterative. Testing was not the end of development; it was a way to collect information and improve the next version.

---

## 5. Looking for Improvements

Once the robot worked, we did not immediately consider it finished. Instead, we looked for possible improvements in every part of the system.

We checked whether the robot could be smaller, lighter, stronger, faster, easier to repair, or more reliable. We also looked at software improvements, such as better sensor processing, smoother steering correction, more stable camera recognition, and cleaner program structure.

This step was important because a working robot is not always an optimized robot. Even if the robot completes a task, small improvements can make it perform more consistently during competition.

We focused especially on parts that caused problems during testing, such as overheating, mechanical friction, sensor inaccuracies, or movement instability.

---

## 6. Making All Possible Improvements

After identifying possible improvements, we implemented as many of them as we realistically could. This included redesigning parts, improving mounts, adjusting tolerances, changing gear ratios, improving cooling, tuning sensor values, and refining software logic.

Some improvements were mechanical, such as making parts stronger or reducing friction. Others were electronic, such as improving cable management or cooling. Software improvements included better calibration, more reliable detection, and improved control behavior.

This step was about turning observations into real changes. Instead of only noting what could be better, we tried to physically improve the robot and then test whether the change actually helped.

---

## 7. Final Testing and Challenge Runs

After making improvements, we performed final system testing. This meant testing the robot as close to competition conditions as possible.

We ran the robot through the actual challenge tasks and checked whether it could perform reliably from start to finish. During these tests, we observed movement accuracy, sensor reactions, turning behavior, camera detection, battery performance, and overall consistency.

If the robot failed or showed a weakness, we returned to step 5 and looked for further improvements. This helped us refine the robot until it became more stable and competition-ready.

Final testing was important because a robot may work once, but competition requires repeatability. The robot needs to perform reliably multiple times, not only under perfect conditions.

---

## 8. Bringing It to Competition

The final step was preparing the robot for competition. At this point, the goal was not to make major experimental changes, but to make sure the robot was complete, reliable, and ready to run.

This included checking all screws, wires, printed parts, sensors, batteries, software files, and spare components. We also made sure the robot could be transported safely and assembled or repaired quickly if needed.

By the time we brought the robot to compete, it had already gone through multiple cycles of design, testing, improvement, and final validation. This gave us more confidence in the system, because the robot was not only designed theoretically, but tested and improved through real experience.

Overall, our development process was based on continuous iteration. Every test gave us feedback, every problem led to a design improvement, and every improvement brought the robot closer to a reliable final version.

---

# Version History / Iteration Log

| Version | Main issue | Change made | Result |
|---|---|---|---|
| V1: First drivetrain concept | No proper mounting system, poor gear fit, unsuitable 45:1 gear ratio, weak electronics mounting, and too small turning radius | First full redesign | Led to V2 |
| V2: First hexagonal mounting system | Steering mechanism was not centered, gears did not fit well, and sensor mounts caused issues | Redesigned the steering and sensor mounts | Led to V3 |
| V3: Second hexagonal mounting system | Gear fit was still unreliable, driveshaft was too low, gear ratios were unsuitable, and there was no battery mount | Completely redesigned the rear section and partially redesigned the front | Led to V4 |
| V4: Final design | Slightly too much friction in moving parts | Added lubricant and filed down moving parts | Competition version |

---

# Build Instructions

The build process of the robot follows a logical order: first the mechanical parts are manufactured, then the electronics are prepared, the components are mounted, the software is uploaded, and finally the whole system is tested. This order is important because each step depends on the previous one being completed correctly.

The general build process is:

1. 3D print the CAD files.
2. Solder and prepare the electronic components.
3. Mount the mechanical parts.
4. Install the electronics onto the chassis.
5. Upload the software to the onboard computer.
6. Configure, calibrate, and test the full system.

---

# CAD Files

The `models/` folder contains the CAD files for the main printable and manufacturable robot parts.

| Part | Purpose |
|---|---|
| Chassis- Drivetrain -Raspberry Pi - Battery mounts | Holds the two metal rods, and most of the components and form the base structure |
| Steering parts | Create the Ackermann steering mechanism |
| Sensor mounts | Hold the ToF sensors and camera in fixed positions |
---
## Hardware Assembly

The first step is to 3D print all custom CAD parts. These include the chassis mounts, drivetrain mounts, sensor mounts, Raspberry Pi mount, steering parts, and any other custom brackets used in the robot. After printing, the parts should be checked for defects, incorrect dimensions, weak layers, or rough surfaces.

Some printed parts may require small adjustments before assembly. This can include sanding, filing, drilling, or slightly widening holes. This is normal because 3D-printed parts are not always perfectly accurate, especially when tight tolerances are used.

After the printed parts are prepared, the mechanical structure can be assembled. The metal rods are used as the main chassis base, and the custom mounts are attached to them. The steering system, drivetrain, differential, gears, wheels, and driveshaft should be installed carefully, making sure that all moving parts rotate freely.

Once the mechanical parts are assembled, the electronics can be prepared. This includes soldering wires, connectors, motor driver connections, sensor cables, power connections, and any required headers. All solder joints should be checked to make sure they are strong and not shorted.

After soldering, the electronics are mounted onto the robot. The Raspberry Pi, motor driver, sensors, battery, camera, and wiring should be placed securely. Cable management is important because loose wires can touch moving parts, block the camera, or disconnect during movement.

---

## Software Installation

After the hardware is assembled, the software can be installed on the Raspberry Pi. The Raspberry Pi should have the required operating system installed and configured before uploading the robot code.

The repository should be copied onto the Raspberry Pi, usually through SSH. SSH allows the robot to be accessed remotely from another computer, so code can be uploaded and tested without connecting a monitor and keyboard directly to the robot.

The required Python libraries must be installed using the project’s setup files or requirements file. These libraries are needed for GPIO control, camera processing, sensor communication, motor control, and web streaming.

The software installation process includes:

1. Copying the project files to the Raspberry Pi.
2. Installing the required system packages.
3. Installing the Python dependencies.
4. Enabling required interfaces such as I²C, camera support, and PWM.
5. Checking that the main program can start without missing-library errors.

---

## Configuration

The Raspberry Pi configuration has to be checked. I²C must be enabled so the sensors can communicate with the Raspberry Pi. Camera support must be enabled so the Pi Camera can work. PWM configuration is also needed for reliable motor and servo control.

The camera color filters may also need adjustment depending on lighting conditions. HSV values for colors such as orange, blue, red, and green should be tuned so the robot detects the correct markings and objects.

Good configuration is important because even a correctly assembled robot can behave incorrectly if the software values do not match the real hardware.

---

## Calibration

Calibration improves the accuracy of the robot before testing or running the challenge. Since sensors and mechanical parts are never perfectly accurate, calibration helps reduce errors.

The gyroscope should be calibrated at startup while the robot is standing still. This allows the program to measure the sensor’s offset and reduce gyro drift. Drift is when the measured angle slowly changes even though the robot is not rotating.

The ToF distance sensors should also be checked using known distances. By comparing the measured values with real distances, the average error can be found and corrected in software.

The motor encoder should be calibrated by moving the robot a known distance and comparing it with the distance calculated by the software. This helps adjust the conversion factor between encoder ticks and centimeters.

The camera system should be calibrated by testing the color detection under the expected lighting conditions. If the camera does not recognize the correct colors, the HSV ranges should be adjusted.

Important calibration steps:

1. Keep the robot still and calibrate the gyroscope.
2. Test ToF sensors at known distances.
3. Check encoder distance calculation.
4. Tune HSV color filters for the camera.
5. Test steering center and maximum steering angles.
6. Confirm that the robot reacts correctly to sensor input.

---

## Testing

After assembly, installation, configuration, and calibration, the robot must be tested. Testing should start with individual components, then move to full-system tests.

First, the motors and steering should be tested separately. Then the sensors should be tested one by one. The camera stream should also be checked to confirm that the robot sees the track correctly.

After individual tests, the complete robot should be tested as one system. During this stage, the robot should be able to move, steer, read sensors, process camera data, and react correctly at the same time.

If problems appear during testing, the build process may return to an earlier step. For example, a mechanical issue may require redesigning or reprinting a part, while a sensor issue may require recalibration or software changes.

The final goal of testing is to confirm that the robot is reliable, repeatable, and ready for challenge runs.

## Rejected design choices

| Option considered  | Why we rejected it                                | Final choice        |
| ------------------ | ------------------------------------------------- | ------------------- |
| Larger chassis     | Easier wiring, but worse turning and less margin  | Compact chassis     |
| 1:1.5 gear ratio   | Too little torque, motor could not start reliably | ~1:6 reduction      |
| Ultrasonic sensors | Larger, slower, less precise at short range       | ToF sensors         |
| No cooling         | Pi overheated during long tests                   | Fan + cooling board |
| Skid steering      | Less realistic, more slip                         | Ackermann steering  |

---

## Points of failure /  Risk analysis table

| Risk                     | Cause                      | Effect                | Prevention / solution              |
| ------------------------ | -------------------------- | --------------------- | ---------------------------------- |
| Raspberry Pi overheating | High CPU load + no cooling | Camera/control crash  | Fan and cooling board              |
| Gyro drift               | IMU offset accumulates     | Wrong heading         | Startup calibration                |
| Wheel slip               | Low traction surface       | Bad odometry          | ToF + camera correction            |
| ToF false reading        | Sunlight/reflection        | Wrong wall distance   | Indoor calibration + sensor fusion |
| Camera color error       | Lighting changes           | Wrong block detection | HSV tuner                          |
| Gear friction            | 3D printed drivetrain      | Power loss / heating  | Lubrication + filing               |


---
# Repository Structure

```text
WRO_26_FE_FRT_neoncso/
│
├── README.md
├── .gitignore
│
├── models/
│   └── 3D models and manufacturing files for printed or machined robot parts
│
├── other/
│   └── Additional technical documentation and supporting files
│
├── schemes/
│   └── Wiring diagrams and electronic connection schemes
│
├── t-photos/
│   └── Team photos required for the WRO documentation
│
├── v-photos/
│   └── Vehicle photos from different angles
│
├── video/
│   └── Driving demonstration video link or video documentation
│
└── src/
    │
    ├── README.md
    ├── __init__.py
    ├── 99-wro.rules
    ├── config.py
    ├── config.txt
    ├── open.py
    ├── obstacle.py
    ├── test.py
    ├── setup.py
    ├── setup.sh
    ├── start.sh
    ├── requirements.txt
    │
    └── utils/
        │
        ├── hsv_tuner/
        │   └── HSV color calibration tools
        │
        ├── gyro.py
        ├── image_proc.py
        ├── log.py
        ├── movement.py
        ├── stream.py
        └── tof.py
```

---

# Media

## Robot Photos

Robot photos from different angles are included in the `v-photos/` folder.

## Team Photos

Team photos are included in the `t-photos/` folder.

## Videos

Driving demonstration videos are included in the `video/` folder.

- Open Challenge video: `video/open_challenge`
- Obstacle Challenge video: `video/obstacle_challenge`

