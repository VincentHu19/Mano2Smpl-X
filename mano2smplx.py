import torch
import numpy as np
from scipy.spatial.transform import Rotation as R

def compute_global_rotation(pose_axis_anges, joint_idx):
    """
    calculating joints' global rotation
    Args:
        pose_axis_anges (np.array): SMPLX's local pose (22,3)
    Returns:
        np.array: (3, 3)
    """
    global_rotation = np.eye(3)
    parents = [-1,  0,  0,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  9,  9, 12, 13, 14, 16, 17, 18, 19]
    while joint_idx != -1:
        joint_rotation = R.from_rotvec(pose_axis_anges[joint_idx]).as_matrix()
        global_rotation = joint_rotation @ global_rotation
        joint_idx = parents[joint_idx]
    return global_rotation

M = np.diag([-1, 1, 1])                                                                                                              # Preparing for the left hand switch

# Assuming that your data are stored in gvhmr_smplx_params and hamer_mano_params
full_body_pose = torch.concatenate((gvhmr_smplx_params["global_orient"], gvhmr_smplx_params["body_pose"].reshape(21, 3)), dim=0)     # gvhmr_smplx_params["global_orient"]: (3, 3)
left_elbow_global_rot = compute_global_rotation(full_body_pose, 18) # left elbow IDX: 18
right_elbow_global_rot = compute_global_rotation(full_body_pose, 19) # left elbow IDX: 19

left_wrist_global_rot = hamer_mano_params["global_orient"][0].cpu().numpy()                                                          # hamer_mano_params["global_orient"]: (2, 3, 3)
left_wrist_global_rot = M @ left_wrist_global_rot @ M                                                                                # mirror switch
left_wrist_pose = np.linalg.inv(left_elbow_global_rot) @ left_wrist_global_rot

right_wrist_global_rot = hamer_mano_params["global_orient"][1].cpu().numpy()
right_wrist_pose = np.linalg.inv(right_elbow_global_rot) @ right_wrist_global_rot

left_wrist_pose_vec = R.from_matrix(left_wrist_pose).as_rotvec()
right_wrist_pose_vec = R.from_matrix(right_wrist_pose).as_rotvec()

left_hand_pose = np.ones(45)
right_hand_pose = np.ones(45)
for i in range(15):
    left_finger_pose = M @ hamer_mano_params["hand_pose"][0][i].cpu().numpy() @ M                                                    # hamer_mano_params["hand_pose"]: (2, 15, 3, 3)
    left_finger_pose_vec = R.from_matrix(left_finger_pose).as_rotvec()
    left_hand_pose[i*3: i*3+3] = left_finger_pose_vec
    
    right_finger_pose = hamer_mano_params["hand_pose"][1][i].cpu().numpy()
    right_finger_pose_vec = R.from_matrix(right_finger_pose).as_rotvec()
    right_hand_pose[i*3: i*3+3] = right_finger_pose_vec

gvhmr_smplx_params["body_pose"][57: 60] = left_wrist_pose_vec
gvhmr_smplx_params["body_pose"][60: 63] = right_wrist_pose_vec
gvhmr_smplx_params["left_hand_pose"] = left_hand_pose
gvhmr_smplx_params["right_hand_pose"] = right_hand_pose
