<?xml version="1.0"?>
<robot name="industrial_arm">

  <!-- MATERIALS -->
  <material name="blue">
    <color rgba="0.1 0.3 0.8 1"/>
  </material>

  <material name="orange">
    <color rgba="1 0.4 0.05 1"/>
  </material>

  <material name="grey">
    <color rgba="0.5 0.5 0.5 1"/>
  </material>

  <!-- LINK 1: BASE -->
  <link name="base_link">
    <visual>
      <origin xyz="0 0 0.05"/>
      <geometry>
        <cylinder radius="0.075" length="0.1"/>
      </geometry>
      <material name="grey"/>
    </visual>

    <collision>
      <origin xyz="0 0 0.05"/>
      <geometry>
        <cylinder radius="0.075" length="0.1"/>
      </geometry>
    </collision>
  </link>

  <!-- LINK 2: SHOULDER -->
  <link name="shoulder_link">
    <visual>
      <origin xyz="0 0 0.075"/>
      <geometry>
        <cylinder radius="0.055" length="0.15"/>
      </geometry>
      <material name="blue"/>
    </visual>

    <collision>
      <origin xyz="0 0 0.075"/>
      <geometry>
        <cylinder radius="0.055" length="0.15"/>
      </geometry>
    </collision>
  </link>

  <!-- JOINT 1: BASE ROTATION -->
  <joint name="joint1" type="revolute">
    <parent link="base_link"/>
    <child link="shoulder_link"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14"
           effort="100" velocity="1"/>
  </joint>

  <!-- LINK 3: UPPER ARM -->
  <link name="upper_arm_link">
    <visual>
      <origin xyz="0.125 0 0"/>
      <geometry>
        <box size="0.25 0.05 0.05"/>
      </geometry>
      <material name="orange"/>
    </visual>

    <collision>
      <origin xyz="0.125 0 0"/>
      <geometry>
        <box size="0.25 0.05 0.05"/>
      </geometry>
    </collision>
  </link>

  <!-- JOINT 2: SHOULDER ROTATION -->
  <joint name="joint2" type="revolute">
    <parent link="shoulder_link"/>
    <child link="upper_arm_link"/>
    <origin xyz="0 0 0.15" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57"
           effort="100" velocity="1"/>
  </joint>

  <!-- LINK 4: FOREARM -->
  <link name="forearm_link">
    <visual>
      <origin xyz="0.1 0 0"/>
      <geometry>
        <box size="0.2 0.04 0.04"/>
      </geometry>
      <material name="blue"/>
    </visual>

    <collision>
      <origin xyz="0.1 0 0"/>
      <geometry>
        <box size="0.2 0.04 0.04"/>
      </geometry>
    </collision>
  </link>

  <!-- JOINT 3: ELBOW ROTATION -->
  <joint name="joint3" type="revolute">
    <parent link="upper_arm_link"/>
    <child link="forearm_link"/>
    <origin xyz="0.25 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-2.0" upper="2.0"
           effort="80" velocity="1"/>
  </joint>

  <!-- LINK 5: END EFFECTOR -->
  <link name="end_effector_link">
    <visual>
      <origin xyz="0.04 0 0"/>
      <geometry>
        <box size="0.08 0.06 0.04"/>
      </geometry>
      <material name="orange"/>
    </visual>

    <collision>
      <origin xyz="0.04 0 0"/>
      <geometry>
        <box size="0.08 0.06 0.04"/>
      </geometry>
    </collision>
  </link>

  <!-- JOINT 4: WRIST ROTATION -->
  <joint name="joint4" type="revolute">
    <parent link="forearm_link"/>
    <child link="end_effector_link"/>
    <origin xyz="0.2 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57"
           effort="50" velocity="1"/>
  </joint>

</robot>
