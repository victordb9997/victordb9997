// bryce_neon_valley.pov — Bryce-style sunset valley with chrome sentinels,
// glass river beads, and a neon horizon. Designed for AI re-dressing.
#include "retro90s.inc"

Retro_Sky_Gradient(rgb <0.12,0.05,0.34>, rgb <1.0,0.48,0.16>)
Retro_Sun(<-0.55,0.72,-0.35>, rgb <1.0,0.78,0.45>)

#declare ValleyStone = texture {
  pigment {
    gradient y
    color_map {
      [0.00 rgb <0.20,0.10,0.25>]
      [0.35 rgb <0.40,0.18,0.35>]
      [0.70 rgb <0.88,0.46,0.18>]
      [1.00 rgb <1.00,0.86,0.55>]
    }
    turbulence 0.25
    scale 6
  }
  finish { ambient 0.24 diffuse 0.72 phong 0.25 phong_size 30 }
}

Retro_Fractal_Terrain(3.2, 9.0, ValleyStone)

// Mirror river running into the valley.
box {
  <-1.1,0.05,-30>, <1.1,0.10,35>
  texture {
    pigment { color rgb <0.10,0.32,0.80> filter 0.35 }
    finish { ambient 0.25 diffuse 0.2 reflection { 0.55 } phong 0.9 phong_size 100 }
  }
}

// Chrome canyon sentinels with re-dressable accent colors.
#declare AccentA = rgb <0.35,1.00,0.92>;
#declare AccentB = rgb <1.00,0.22,0.72>;

#macro Sentinel(Pos, Radius, Height, Accent)
  union {
    cylinder { <0,0,0>, <0,Height,0>, Radius Retro_Chrome(rgb <0.92,0.92,1.0>) }
    torus { Radius*1.08, Radius*0.08 rotate x*90 translate <0,Height*0.34,0> Retro_Plastic(Accent) }
    torus { Radius*1.08, Radius*0.08 rotate x*90 translate <0,Height*0.68,0> Retro_Plastic(Accent) }
    sphere { <0,Height+Radius*0.9,0>, Radius*0.95 Retro_Glass(Accent) }
    translate Pos
  }
#end

Sentinel(<-4.5,0.0,8>, 0.45, 4.6, AccentA)
Sentinel(< 4.8,0.0,10>, 0.55, 5.4, AccentB)
Sentinel(<-7.0,0.0,18>, 0.35, 3.6, AccentB)
Sentinel(< 7.2,0.0,20>, 0.38, 3.9, AccentA)

// Floating glass river markers.
#local I = 0;
#while (I < 7)
  sphere {
    <0,0.85, -6 + I*4.2>, 0.34
    Retro_Glass(rgb <0.55,0.95,1.0>)
  }
  #local I = I + 1;
#end

Retro_Camera(<-8.0,5.2,-14.0>, <0,1.8,10.0>)
