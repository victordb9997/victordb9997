// chrome_text_logo_stage.pov — 90s demo-scene logo stage: chrome letters,
// colored glass pylons, checker floor, and hard specular highlights.
#include "retro90s.inc"

Retro_Sky_Gradient(rgb <0.02,0.02,0.12>, rgb <0.55,0.12,0.75>)
Retro_Sun(<-0.35,0.62,-0.45>, rgb <0.95,0.98,1.0>)
Retro_Checker_Floor(rgb <0.92,0.92,1.0>, rgb <0.04,0.04,0.08>, 0.45)

#declare HotPink = rgb <1.0,0.10,0.62>;
#declare Cyan    = rgb <0.05,0.95,1.0>;
#declare Gold    = rgb <1.0,0.72,0.18>;

// A chunky primitive text-logo spelling RTC with chrome/glass demo aesthetics.
union {
  // R
  box { <-3.9,0.0,0>, <-3.3,2.6,0.55> Retro_Chrome(rgb <0.95,0.95,1.0>) }
  torus { 0.48,0.18 rotate x*90 scale <1.15,1.0,1.0> translate <-2.95,2.05,0.28> Retro_Chrome(rgb <0.95,0.95,1.0>) }
  cylinder { <-3.25,1.05,0.28>, <-2.35,0.0,0.28>, 0.18 Retro_Chrome(rgb <0.95,0.95,1.0>) }
  // T
  box { <-1.45,2.15,0>, <0.15,2.75,0.55> Retro_Chrome(rgb <0.95,0.95,1.0>) }
  box { <-0.72,0.0,0>, <-0.18,2.2,0.55> Retro_Chrome(rgb <0.95,0.95,1.0>) }
  // C
  torus { 0.95,0.22 rotate x*90 translate <1.75,1.35,0.28> Retro_Chrome(rgb <0.95,0.95,1.0>) }
  box { <2.05,1.05,-0.1>, <3.0,1.75,0.75> texture { pigment { color rgbt <0,0,0,1> } } }

  rotate y*(sin(clock*2*pi)*8)
  translate <0,0.1,6.5>
}

// Glass pylons and neon orb accents.
#macro Pylon(X, Col)
  union {
    cone { <X,0,7.0>, 0.40, <X,3.2,7.0>, 0.12 Retro_Glass(Col) }
    sphere { <X,3.55,7.0>, 0.32 Retro_Plastic(Col) }
  }
#end

Pylon(-5.0, HotPink)
Pylon( 5.0, Cyan)
Pylon(-1.4, Gold)
Pylon( 1.4, Gold)

// Reflective back wall for the logo to catch itself.
box {
  <-8,0,10.2>, <8,5.2,10.35>
  texture {
    pigment { color rgb <0.02,0.02,0.06> }
    finish { ambient 0.12 diffuse 0.25 reflection { 0.35 } phong 0.6 phong_size 70 }
  }
}

Retro_Camera(<0,3.0,-6.2>, <0,1.55,6.6>)
