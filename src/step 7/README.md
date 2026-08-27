**Overview**

Step 7 evaluates the steering geometry and turn radii for the robot using constant-radius arc tests. By driving specified step counts at fixed servo angles, the procedure calculates turn dynamics using a three-point positioning method ($P_1, P_2, P_3$).

---

**Robot Configuration & Calibration Data**

* **Physical Metrics:**
* **Wheelbase ($L$):** 167 mm
* **Rear Track Width ($T$):** 139 mm
* **Wheel Diameter / Width:** 56 mm / 27 mm


* **Control Mapping:**
* **Servo Center:** 82 (Straight)
* **Lower Servo Values ($< 82$):** Turn **RIGHT**
* **Higher Servo Values ($> 82$):** Turn **LEFT**
* **Motor Speed:** 600 steps/sec | **Acceleration:** 2000 steps/sec²



---

**Test Method & Execution**

1. **Firmware Setup:** PlatformIO code (`step7_constant_radius_test/src/main.cpp`) controls steering via servo angles and distance via stepper steps, executed with a 5-second countdown (`GO`).
2. **Three-Point Geometry Measurement:**

* The rear axle midpoint is marked on the floor at the start ($P_1$), after the first run ($P_2$), and after an identical second run ($P_3$).
* Straight-line distances between points ($d_{12}, d_{23}, d_{13}$) are recorded to derive the exact turning arc radii without manually tracing curved paths.

---

**Experimental Data & Calculated Results**

*(Target Steps = 1800 for all trials)*

| Steering Angle | Direction | $P_1 \to P_2$ ($d_{12}$) | $P_2 \to P_3$ ($d_{23}$) | $P_1 \to P_3$ ($d_{13}$) | Calculated Turning Radius |
| --- | --- | --- | --- | --- | --- |
| **75** | Right | 1067 mm | 1067 mm | 1945 mm | — |
| **75** | Right | 1070 mm | 1049 mm | 1930 mm | — |
| **75** | Right | 1030 mm | 1060 mm | 1890 mm | — |
| **66** | Right | 932 mm | 932 mm | 1050 mm | **564.0 mm** |
| **90** | Left | 1048 mm | 1065 mm | 1962 mm | — |
| **90** | Left | 1054 mm | 1040 mm | 1961 mm | — |
| **90** | Left | 1067 mm | 1052 mm | 1971 mm | — |
| **105** | Left | 830 mm | 820 mm | 547 mm | **437.3 mm** |

---

**Key Takeaways**

* **Turn Radii Output:**
* **Angle 66 (Right):** Yields a **564.0 mm** turn radius.
* **Angle 105 (Left):** Yields a sharper **437.3 mm** turn radius.


* **Updated Drive Calibration:**
* Across the 1800-step test runs (averaging ~1085 mm path length), the drive calibration was updated to **1660 steps/meter** (`constexpr long STEPS_PER_METER = 1660L;`).
* *Note:* This revised distance conversion must be verified later with a direct straight-line run.
