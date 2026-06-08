// glass_city_skyline.pov — crystalline downtown skyline with colored glass,
// glowing window strips, and an infinite reflective plaza.
#include "retro90s.inc"

Retro_Sky_Gradient(rgb <0.00,0.06,0.24>, rgb <0.10,0.82,0.96>)
Retro_Sun(<0.25,0.8,-0.35>, rgb <0.82,0.96,1.0>)
Retro_Checker_Floor(rgb <0.06,0.08,0.16>, rgb <0.24,0.34,0.44>, 0.38)

#declare WindowGlow = texture { pigment { rgb <0.55,1.0,1.0> } finish { ambient 1.8 diffuse 0.1 } }

#macro Tower(X, Z, W, H, Tint, Kind)
  union {
    #if (Kind = 0)
      box { <-W,0,-W>, <W,H,W> Retro_Glass(Tint) }
    #else
      cone { <0,0,0>, W*1.5, <0,H,0>, W*0.55 Retro_Glass(Tint) }
    #end

    // Front luminous strips.
    #local Y = 0.65;
    #while (Y < H-0.25)
      box { <-W*0.70,Y,-W-0.035>, <W*0.70,Y+0.10,-W-0.015> texture { WindowGlow } }
      #local Y = Y + 0.58;
    #end

    // Floating chrome roof cap.
    sphere { <0,H+0.34,0>, W*0.42 scale <1,0.45,1> Retro_Chrome(rgb <0.86,0.92,1.0>) }
    translate <X,0,Z>
  }
#end

Tower(-6.0,12,0.70,4.2,rgb <0.35,0.95,1.0>,0)
Tower(-4.1,10,0.95,6.0,rgb <0.65,0.35,1.0>,1)
Tower(-1.9,13,0.82,5.2,rgb <0.20,0.92,0.75>,0)
Tower( 0.2,11,1.15,7.2,rgb <0.95,0.25,0.55>,0)
Tower( 2.8,13,0.90,5.7,rgb <0.25,0.70,1.0>,1)
Tower( 5.5,10,0.78,4.8,rgb <1.0,0.82,0.22>,0)

// Overhead cyber-arches.
#local A = -5;
#while (A <= 5)
  torus {
    2.2, 0.06
    rotate x*90
    scale <1,0.18,1>
    translate <A,4.4,9.5>
    Retro_Plastic(rgb <0.22,1.0,0.92>)
  }
  #local A = A + 2.5;
#end

Retro_Orbit_Camera(13, 4.1, <0,3.0,11.5>)
