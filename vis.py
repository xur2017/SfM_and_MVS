
import read_write_model
import open3d as o3d
import numpy as np

def apply_transform(xyz, transform):
    """Applies a rigid transform to an (N, 3) pointcloud.
    """
    xyz_h = np.hstack([xyz, np.ones((len(xyz), 1), dtype=np.float32)])
    xyz_t_h = (transform @ xyz_h.T).T
    return xyz_t_h[:, :3]

obj_list = []
pcd1 = o3d.io.read_point_cloud("./dense/fused.ply")
obj_list.append(pcd1)

cameras, images, points3D = read_write_model.read_model("./dense/sparse")
cam = cameras[1]
im_w, im_h = cam.width, cam.height
fx, fy, cx, cy = cam.params
# xyz = []
# rgb = []
# for k, v in points3D.items():
#     #print(k)
#     xyz.append(v.xyz)
#     rgb.append(v.rgb)
# xyz = np.asarray(xyz)
# rgb = np.asarray(rgb)
# rgb[:,:3] = np.array([0,0,255])
# pcd1 = o3d.geometry.PointCloud()
# pcd1.points = o3d.utility.Vector3dVector(xyz)
# pcd1.colors = o3d.utility.Vector3dVector(rgb/255)
# pcd1, ind = pcd1.remove_statistical_outlier(nb_neighbors=20, std_ratio=0.75)
# obj_list.append(pcd1)

color=[0.8, 0.2, 0.8]
z = 0.2
for k, v in images.items():
    #print( k )
    R = read_write_model.qvec2rotmat(v.qvec)
    t = v.tvec
    # invert
    t = -R.T @ t
    R = R.T
    
    cam_pose = np.column_stack((R, t))
    cam_pose = np.vstack((cam_pose, (0, 0, 0, 1)))
    
    cam_pts0 = np.array([
        (np.array([0, 0, 0, im_w, im_w])-cx)*np.array([0, z, z, z, z])/fx,
        (np.array([0, 0, im_h, 0, im_h])-cy)*np.array([0, z, z, z, z])/fy,
         np.array([0, z, z, z, z])
    ]).T

    cam_pts1 = apply_transform(cam_pts0, cam_pose)
    lines = [[0, 1],[0, 2],[0, 3],[0, 4],[1,2],[1,3],[4,2],[4,3]]
    line_set = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(cam_pts1),
        lines=o3d.utility.Vector2iVector(lines),)
    obj_list.append(line_set)

    w = abs(cam_pts0[1][0]-cam_pts0[3][0])
    h = abs(cam_pts0[1][1]-cam_pts0[2][1])
    plane = o3d.geometry.TriangleMesh.create_box(w, h, depth=1e-6)
    plane.paint_uniform_color(color)
    plane.translate([cam_pts0[1][0], cam_pts0[1][1], cam_pts0[1][2]])
    plane.transform(cam_pose)
    obj_list.append(plane)

o3d.visualization.draw_geometries(obj_list)
