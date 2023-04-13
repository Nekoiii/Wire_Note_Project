#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电脑键盘-钢琴键映射表
"""

import pygame

#按键映射表
keys_map = {
    pygame.K_TAB: {'note_name': 'E3', 'lily_note': 'e,'},
    pygame.K_q: {'note_name': 'F3', 'lily_note': 'f,'},
    pygame.K_w: {'note_name': 'G3', 'lily_note': 'g,'},
    pygame.K_e: {'note_name': 'A3', 'lily_note': 'a,'},
    pygame.K_r: {'note_name': 'B3', 'lily_note': 'b,'},
    pygame.K_t: {'note_name': 'C4', 'lily_note': 'c'},
    pygame.K_y: {'note_name': 'D4', 'lily_note': 'd'},
    pygame.K_u: {'note_name': 'E4', 'lily_note': 'e'},
    pygame.K_i: {'note_name': 'F4', 'lily_note': 'f'},
    pygame.K_o: {'note_name': 'G4', 'lily_note': 'g'},
    pygame.K_p: {'note_name': 'A4', 'lily_note': 'a'},
    pygame.K_LEFTBRACKET: {'note_name': 'B4', 'lily_note': 'b'},
    pygame.K_RIGHTBRACKET: {'note_name': 'C4', 'lily_note': 'c\''},
    pygame.K_6: {'note_name': 'C#4', 'lily_note': 'cis'},
    pygame.K_7: {'note_name': 'D#4', 'lily_note': 'dis'},
    pygame.K_9: {'note_name': 'F#4', 'lily_note': 'fis'},
    pygame.K_0: {'note_name': 'G#4', 'lily_note': 'gis'},
    pygame.K_MINUS: {'note_name': 'A#4', 'lily_note': 'ais'}
}










