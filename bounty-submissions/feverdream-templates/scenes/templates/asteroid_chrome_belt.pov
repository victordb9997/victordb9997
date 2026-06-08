// asteroid_chrome_belt.pov — chrome asteroid belt with glass comets and a
// neon-ringed planet, pure 1994 raytrace poster energy.
#include "retro90s.inc"

Retro_Sky_Gradient(rgb <0.00,0.00,0.05>, rgb <0.10,0.02,0.18>)
Retro_Sun(<-0.45,0.62,-0.50>, rgb <0.70,0.86,1.0>)

// Star field backdrop.
#local S = 0;
#while (S < 80)
  sphere {
    <sin(S*12.989)*18, 2 + abs(cos(S*7.17))*13, 18 + cos(S*5.31)*18>, 0.035
    texture { pigment { rgb <0.85,0.92,1.0> } finish { ambient 1.4 diffuse 0 } }
  }
  #local S = S + 1;
#end

// Dark reflective space plane far below catches object glints.
plane {
  y, -1.4
  texture {
    pigment { color rgb <0.01,0.01,0.025> }
    finish { ambient 0.08 diffuse 0.15 reflection { 0.20 } }
  }
}

// Ringed glass planet.
union {
  sphere { <0,2.4,12>, 2.0 Retro_Glass(rgb <0.18,0.62,1.0>) }
  torus { 2.85, 0.10 rotate x*68 translate <0,2.4,12> Retro_Chrome(rgb <0.95,0.76,0.36>) }
  torus { 3.35, 0.06 rotate x*68 translate <0,2.4,12> Retro_Plastic(rgb <0.95,0.18,0.82>) }
}

// Faceted asteroids using scaled spheres and hard rotations.
#macro Rock(Pos, Size, Tint)
  sphere {
    0, 1
    scale <Size*1.35, Size*0.70, Size>
    rotate <Pos.x*9, Pos.z*13, Pos.y*17>
    translate Pos
    Retro_Chrome(Tint)
  }
#end

#local I = 0;
#while (I < 18)
  #local Angle = I*20 + clock*80;
  #local R = 5.2 + mod(I,4)*0.72;
  #local P = <cos(radians(Angle))*R, 2.1 + sin(I*1.3)*1.1, 12 + sin(radians(Angle))*R*0.55>;
  Rock(P, 0.32 + mod(I,5)*0.055, rgb <0.72+mod(I,3)*0.08,0.74,0.82>)
  #local I = I + 1;
#end

// Glass comets crossing the belt.
cylinder { <-5,4.5,8>, <-1.4,2.9,10.5>, 0.08 Retro_Glass(rgb <0.35,1.0,0.95>) }
sphere { <-1.4,2.9,10.5>, 0.34 Retro_Glass(rgb <0.35,1.0,0.95>) }
cylinder { <5,1.0,17>, <1.5,2.4,14.0>, 0.08 Retro_Glass(rgb <1.0,0.25,0.72>) }
sphere { <1.5,2.4,14.0>, 0.34 Retro_Glass(rgb <1.0,0.25,0.72>) }

Retro_Camera(<0,4.1,-7.5>, <0,2.2,12>)
