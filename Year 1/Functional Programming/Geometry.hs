-- to create a module use the module Name () where syntax
module Geometry
( sphereVolume
, sphereArea
) where

sphereVolume :: Float -> Float  
sphereVolume radius = (4.0 / 3.0) * pi * (radius ^ 3)  
  
sphereArea :: Float -> Float  
sphereArea radius = 4 * pi * (radius ^ 2)