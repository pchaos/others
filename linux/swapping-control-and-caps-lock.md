# Swapping Control and Caps Lock

In your home directory, create a file called .Xmodmap (some distros use .xmodmap), and put the following in there: 

``````
!
! Swap Caps_Lock and Control_L
!
remove Lock = Caps_Lock
remove Control = Control_L
keysym Control_L = Caps_Lock
keysym Caps_Lock = Control_L
add Lock = Caps_Lock
add Control = Control_L
``````

Log out and then log back in, and voila! Your keys are swapped. Consider this my contribution to preventing both unnecessary slowdowns and pinky finger strain for people everywhere. :-)

