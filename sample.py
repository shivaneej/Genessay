from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import os
from model import load


def generate_text(keywords):
  print(keywords)
  path = os.getcwd()    
  parser = ArgumentParser(formatter_class = ArgumentDefaultsHelpFormatter)
  parser.add_argument('--data-dir', type = str, default = path, help = 'data directory containing input.txt')
  parser.add_argument('--seed', type = str, default=' '.join(keywords),help = 'seed string for sampling')
  parser.add_argument('--length', type = int, default = int(1.5*len(keywords)) ,help = 'length of the sample to generate') #change the '8' to change number of words
  parser.add_argument('--diversity', type = float, default = 0.01, help = 'Sampling diversity')
  args = parser.parse_args()
  model = load(args.data_dir)
  del args.data_dir
  sentence = model.sample(**vars(args))
  print("test", sentence)
  return sentence

# print("hope", generate_text(['college', '1611005', 'come', 'roll']))

# keywords = []
# keywords = [['roll']]
