import os
import sys

BASE_PATH='/Users/a/code/Wire_Note_Project'
sys.path.append(BASE_PATH)

MODELS_PATH=os.path.join(BASE_PATH,'models')
ASSETS_PATH=os.path.join(BASE_PATH,'assets')
DATASETS_PATH = os.path.join(BASE_PATH,'datasets')



BG_PATH=os.path.join(ASSETS_PATH,'imgs/bg.jpg')
# BGM_PATH=os.path.join(ASSETS_PATH,'audios/musicgen_out-3.mp3')
BGM_PATH=os.path.join(ASSETS_PATH,'audios/test_audio-2.mp3')
MIDI_PATH=os.path.join(ASSETS_PATH,'midi/musicgen_out-3_basic_pitch.mid')

CLASSES = ['cable', 'tower_wooden']
DATASET_PATH = os.path.join(DATASETS_PATH,'ttpla_dataset/data_original_size_v1')





