# How to get the code

Two main websites

https://github.com/johnidm/asm-atari-2600/tree/master

https://forums.atariage.com/topic/256141-disassembling-2600-games/page/4/

# Use the assembly code

##

###

The most basic way of using assembly code is to retrieve the memory mapping of objects and then use linear regression to
know how it correlates to the actual characteristics of object.
To do so, two ways:
Open the code in the editor and go to the variable part

```assembly
;============================================================================
; Z P - V A R I A B L E S
;============================================================================

gameState               = $80
currentShieldGraphics   = $81       ; $81 - $90
neutralZoneMask         = $91
qotileMissileSpeedIndex = $92
yarColor                = $93
qotileStatus            = $94
kernelStatus            = $95
zorlonCannonStatus      = $96
yarStatus               = $97
zorlonCannonVertPos     = $98
zorlonCannonHorizPos    = $99
shieldVertPos           = $9A
shieldSectionHeight     = $9B
```

In this case the $ sign indicates to which memory mapping the variable corresponds to in hexadecimal code and a shift of
80(16), for example the ram emplacements 81 to 91(base 16) corresponds to the state of the shield and with the shift the
values to be used in the code to
track the state of the shield are ram_state[1], ram_state[2]... ram_state[10]

###

On the other sometimes the only thing written is actually the size of the memory allocated to each variable:

```assembly
;===============================================================================
; Z P - V A R I A B L E S
;===============================================================================
livesPat            .byte   ;           number of lives, stored as displayed pattern ($a0 = 3, $80 = 2, $00 = 1)
random              .byte   ;           all scenes are generated randomly with this
random2             .byte   ;           used for random object animation
joystick            .byte   ;           stores joystick directions
fireButton          .byte   ;           stores fire button state
hitLiana            .byte   ;           Harry collided with liana? (bit 6 = 1 -> yes)
cxHarry             .byte   ;           Harry's collisions (stored but _never_ read!)
SS_XOR              .byte   ;           change colors in screensaver mode (0/$01..$ff)
SS_Mask             .byte   ;           darker colors in screensaver mode ($ff/$f7)
colorLst            ds 9    ;           some (mostly constant!?) colors
lianaBottom         .byte   ;           bottom row of liana
objectType          .byte   ;           type of the objects on the ground (hazards & treasures)
sceneType           .byte   ;           type of the scene (0..7
HMFineLst           ds 3    ;           fine positioning value for: Harry, ground-object, underground-object
HMCoarseLst         ds 3    ;           coars positioning value for: Harry, ground-object, underground-object
posLeftBranch       .byte   ;           values for positioning left branch graphics
posRightBranch      .byte   ;           values for positioning right branch graphics
ladderFlag          .byte   ;           0 = no ladder, $ff = with ladder
noGameScroll        .byte   ;           0 = game is running
PF2QuickSand        .byte   ;           PF2 data for top quicksand row
PF2Lst              ds 7    ;           copied pit pattern data
objColLst           ds 7    ;           copied object colors

```

Then the first byte correspond to the slot 0 in the memory and so on.
As such, what I like to do is to use a text editor and put an empty line if a variables take two bytes, 2 empty lines if
a variable
takes 3 bytes and so on... So the first line corresponds to ram_state[0], 2nd corresponds to ram_state[1] and so on

For this example that would do:

```assembly
livesPat            .byte   ;           number of lives, stored as displayed pattern ($a0 = 3, $80 = 2, $00 = 1)
random              .byte   ;           all scenes are generated randomly with this
random2             .byte   ;           used for random object animation
joystick            .byte   ;           stores joystick directions
fireButton          .byte   ;           stores fire button state
hitLiana            .byte   ;           Harry collided with liana? (bit 6 = 1 -> yes)
cxHarry             .byte   ;           Harry's collisions (stored but _never_ read!)
SS_XOR              .byte   ;           change colors in screensaver mode (0/$01..$ff)
SS_Mask             .byte   ;           darker colors in screensaver mode ($ff/$f7)
colorLst            ds 9    ;           some (mostly constant!?) colors
2
3
4
5
6
7
8
9
lianaBottom         .byte   ;           bottom row of liana
objectType          .byte   ;           type of the objects on the ground (hazards & treasures)
sceneType           .byte   ;           type of the scene (0..7
HMFineLst           ds 3    ;           fine positioning value for: Harry, ground-object, underground-object
HMCoarseLst         ds 3    ;           coars positioning value for: Harry, ground-object, underground-object
posLeftBranch       .byte   ;           values for positioning left branch graphics
posRightBranch      .byte   ;           values for positioning right branch graphics
ladderFlag          .byte   ;           0 = no ladder, $ff = with ladder
noGameScroll        .byte   ;           0 = game is running
PF2QuickSand        .byte   ;           PF2 data for top quicksand row
PF2Lst              ds 7    ;           copied pit pattern data






objColLst           ds 7    ;           copied object colors
...
```

So by putting it in a code editor I know for example that the liana bottom corresponds to line 19 which means to
ram_state[18]

#### Few notation:

> #### ds n --> n bytes
> #### word --> 2 bytes
> #### ds.w 6 --> 6 words so 12 bytes

#### :warning: Sometimes they can also grouped variables

Such as:

```assembly
fishingPolePFValues     ds 4
;--------------------------------------
fishingPolePF1Values    = fishingPolePFValues
;--------------------------------------
leftFishingPolePF1Value = fishingPolePF1Values
rightFishingPolePF1Value = leftFishingPolePF1Value + 1
fishingPolePF2Values    = fishingPolePFValues + 2
;--------------------------------------
leftFishingPolePF2Value = fishingPolePF2Values
rightFishingPolePF2Value = leftFishingPolePF2Value + 1
```

Which means the group corresponding to fishingPolePFValues has 4 bytes allocated.

1. First part is for leftFishingPolePF1Value which itself is a group composed of
    1. rightFishingPolePF1Value for 1 byte
    2. fishingPolePF2Values for 1 byte
2. Second part is fishingPolePF2Values
    1. leftFishingPolePF2Value for 1 byte
    2. rightFishingPolePF2Value for 1 byte

We know it's a group because the ram slot number is expressed using the ram slot value of another variable in the code

As such when doing the technique with inserting blank lines we can either count fishingPolePFValues as a whole group of
4 bytes and delete the other lines of the group or only keeping rightFishingPolePF1Value for 1 byte, fishingPolePF2Values for 1 byte,
leftFishingPolePF2Value for 1 byte, rightFishingPolePF2Value for 1 byte,
