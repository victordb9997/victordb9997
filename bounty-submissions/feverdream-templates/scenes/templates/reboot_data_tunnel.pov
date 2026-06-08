// reboot_data_tunnel.pov — inside a glowing ReBoot-style data tunnel with
// recursive neon ribs, packet cubes, and a reflective grid floor.
#include "retro90s.inc"

Retro_Sky_Gradient(rgb <0.00,0.02,0.08>, rgb <0.05,0.14,0.32>)
Retro_Sun(<0.0,0.5,-0.7>, rgb <0.55,0.85,1.0>)
Retro_Grid_Floor(rgb <0.10,1.0,0.78>, rgb <0.02,0.04,0.08>, 1.2)

#declare NeonGreen = rgb <0.18,1.00,0.56>;
#declare NeonBlue  = rgb <0.12,0.55,1.00>;
#declare NeonPink  = rgb <1.00,0.12,0.62>;

// Tunnel ribs: square torus-like frames made from cylinders.
#macro Rib(Z, Size, Col)
  union {
    cylinder { <-Size,Size,Z>, < Size,Size,Z>, 0.055 Retro_Plastic(Col) }
    cylinder { <-Size,-Size,Z>, < Size,-Size,Z>, 0.055 Retro_Plastic(Col) }
    cylinder { <-Size,-Size,Z>, <-Size, Size,Z>, 0.055 Retro_Plastic(Col) }
    cylinder { < Size,-Size,Z>, < Size, Size,Z>, 0.055 Retro_Plastic(Col) }
  }
#end

#local Z = 5;
#while (Z < 34)
  #local S = 1.2 + Z*0.075;
  #if (mod(Z,6) < 3)
    Rib(Z, S, NeonGreen)
  #else
    Rib(Z, S, NeonBlue)
  #end
  #local Z = Z + 2;
#end

// Data packets flying toward camera.
#local I = 0;
#while (I < 14)
  box {
    <-0.28,-0.28,-0.28>, <0.28,0.28,0.28>
    Retro_Glass(NeonPink)
    rotate <25+I*9, 40+I*23, 10>
    translate <sin(I*1.7)*2.2, 1.0+cos(I*1.1)*0.7, 6+I*2.1>
  }
  #local I = I + 1;
#end

// Central chrome cursor/ship.
union {
  cone { <0,0,0>, 0.52, <0,0,1.35>, 0.0 Retro_Chrome(rgb <0.9,0.96,1.0>) }
  sphere { <0,0,0>, 0.42 Retro_Glass(rgb <0.32,0.90,1.0>) }
  rotate y*(clock*360)
  translate <0,1.15,4.2>
}

Retro_Camera(<0,1.7,-3.5>, <0,1.3,15>)
