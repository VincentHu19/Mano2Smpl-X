# Mano2Smpl-X

Here we provide a way to fuse MANO parameters into SMPLX. 

Most methods model the human body and hand separately, and it is important to fuse the two parameters. But aligning hand pose and wrist pose is difficult. We decide to share our efforts. The idea is to calculate the global rotation of the elbow and the entire hand, respectively, to get the local pose of the wrist. The pose of the fingers can be transferred directly.  

Our code was tested on [GVHMR](https://github.com/zju3dv/GVHMR) and [hamer](https://github.com/zju3dv/GVHMR). You can also replace the appropriate parts of the code with MANO and SMPLX parameters calculated in other ways. Since hamer uses a right-handed model to represent all hands, we provide left-right hand conversions in our code

Make sure to set **flat_hand_mean=True** in SMPLX!


![messi_out](https://github.com/user-attachments/assets/878fc732-2ba4-41f7-9219-816f4cf9fda1)
