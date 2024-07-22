
import os

base_path = "C:/E/LocalGithub/sfm-mvs-dev"

# sfm step
cmdline = f"{base_path}/colmap/COLMAP.bat feature_extractor \
    --database_path {base_path}/database.db \
    --image_path {base_path}/images \
    --SiftExtraction.max_image_size 1600 \
    --SiftExtraction.max_num_features 4096"
os.system(cmdline)

cmdline = f"{base_path}/colmap/COLMAP.bat exhaustive_matcher \
    --database_path {base_path}/database.db"
os.system(cmdline)

cmdline = f"{base_path}/colmap/COLMAP.bat mapper \
    --database_path {base_path}/database.db \
    --image_path {base_path}/images \
    --output_path {base_path}/sparse"
os.system(cmdline)

# mvs step
cmdline = f"{base_path}/colmap/COLMAP.bat image_undistorter \
    --image_path {base_path}/images \
    --input_path {base_path}/sparse/0 \
    --output_path {base_path}/dense \
    --output_type COLMAP \
    --max_image_size 1600"
os.system(cmdline)

cmdline = f"{base_path}/colmap/COLMAP.bat patch_match_stereo \
    --workspace_path {base_path}/dense \
    --workspace_format COLMAP \
    --PatchMatchStereo.geom_consistency 0"
os.system(cmdline)

cmdline = f"{base_path}/colmap/COLMAP.bat stereo_fusion \
    --workspace_path {base_path}/dense \
    --workspace_format COLMAP \
    --input_type photometric \
    --output_path {base_path}/dense/fused.ply"
os.system(cmdline)