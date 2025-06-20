#----------------------
# Author : Serge Zaugg
# Description : Example of xco usage in practice 
#----------------------

# Make an instance of the XCO class and define the start path 
import xco 
xc = xco.XCO(start_path = 'd:/xc_real_projects/xc_all_4_pooled')

# # Make rectangular spectrogram with size = 128 freq x 256 time 
# xc.extract_spectrograms(fs_tag = 24000, segm_duration = 0.394 , segm_step = 0.80, win_siz = 256, win_olap = 220.5, max_segm_per_file = 16, equalize = True, colormap='viridis')
# Make long spectrogram 128 freq x 1152 time (1024+128= 1152)
xc.extract_spectrograms(fs_tag = 24000, segm_duration = 1.738, segm_step = 0.95, win_siz = 256, win_olap = 220.00, max_segm_per_file = 20, equalize = True, colormap='viridis')


