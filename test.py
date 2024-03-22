from mortal.engine import MortalEngine
import pathlib
import torch
import numpy as np
from torch.distributions import Normal, Categorical
from typing import *
from mortal.model import Brain, DQN

def get_engine(model_file:str = 'mortal.pth') -> MortalEngine:
    # check if GPU is available
    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')

    # Get the path of control_state_file = current directory / control_state_file
    model_file = pathlib.Path(__file__).parent / model_file
    state = torch.load(model_file, map_location=device)

    mortal = Brain(version=state['config']['control']['version'],
        conv_channels=state['config']['resnet']['conv_channels'],
        num_blocks=state['config']['resnet']['num_blocks']).eval()
    dqn = DQN(version=state['config']['control']['version']).eval()
    mortal.load_state_dict(state['mortal'])
    dqn.load_state_dict(state['current_dqn'])

    engine = MortalEngine(
        mortal,
        dqn,
        is_oracle = False,
        device = device,
        enable_amp = False,
        enable_quick_eval = False,
        enable_rule_based_agari_guard = False,
        name = 'mortal',
        version = state['config']['control']['version'],
    )

    return engine

def test_libriichi():
    import libriichi
    import json
    engine = get_engine()
    mjai_bot = libriichi.mjai.Bot(engine, 0)
    
    botin = {"type":"start_game","id":0}
    json_input = json.dumps(botin)
    react_str = mjai_bot.react(json_input)
    print(react_str)
    
    botin = {"type":"start_kyoku","bakaze":"E","dora_marker":"2s",
        "kyoku":1,"honba":0,"kyotaku":0,"oya":0,
        "scores":[25000,25000,25000,25000],
        "tehais":[
            ["6m","7m","9m","9m","8m","5m","2m","5mr","6m","5s","6s","7s","8s"],
            ["?","?","?","?","?","?","?","?","?","?","?","?","?"],
            ["?","?","?","?","?","?","?","?","?","?","?","?","?"],
            ["?","?","?","?","?","?","?","?","?","?","?","?","?"]
            ]
        }
    json_input = json.dumps(botin)
    react_str = mjai_bot.react(json_input)
    print(react_str)    
    
    # bot_clone = mjai_bot.clone()
    botin = {"type":"tsumo","actor":0,"pai":"F"}
    json_input = json.dumps(botin)
    react_str = mjai_bot.react(json_input)
    print("bot1: ", react_str)
    
    
    # botin = {"type":"tsumo","actor":0,"pai":"C"}
    # json_input = json.dumps(botin).replace('True','true')
    # react_str = bot_clone.react(json_input)
    # print("bot2: ", react_str)
    
    
    
if __name__ == '__main__':
    test_libriichi()