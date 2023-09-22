import os
import sys
import seaborn as sns

BASE_PATH='/Users/a/code/Wire_Note_Project'
sys.path.append(BASE_PATH)

MODELS_PATH=os.path.join(BASE_PATH,'models')
ASSETS_PATH=os.path.join(BASE_PATH,'assets')
DATASETS_PATH = os.path.join(BASE_PATH,'datasets')
OUTPUTS_PATH=os.path.join(BASE_PATH,'runs/outputs')


BG_PATH=os.path.join(ASSETS_PATH,'imgs/bg.jpg')
# BGM_PATH=os.path.join(ASSETS_PATH,'audios/musicgen_out-3.mp3')
BGM_PATH=os.path.join(ASSETS_PATH,'audios/test_audio-2.mp3')
MIDI_PATH=os.path.join(ASSETS_PATH,'midi/musicgen_out-3_basic_pitch.mid')

CLASSES = ['cable', 'tower_wooden']
DATASET_PATH = os.path.join(DATASETS_PATH,'ttpla_dataset/data_original_size_v1')

# Define different colors for each class
CLASSES_COLORS= [(int(r*255), int(g*255), int(b*255)) for r, g, b in
              sns.color_palette('pastel', len(CLASSES))]


