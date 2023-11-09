import csv
class PokemonData:
  # version
  RedGreen = 1
  GoldSilver = 2
  RubySapphire = 3
  DiamondPearl = 4
  BlackWhite = 5
  X__Y__ = 6
  SunMoon = 7
  SordShield = 8

  def __init__(self) -> None:
      self.pokemons = []
      self.make_pokemon_data()

  def make_pokemon_data(self):
    csv_file = open("Pokemons.csv", "r", encoding="utf8", errors="", newline="" )
    # list
    poke_data_all = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    header = next(poke_data_all)
    for poke_data in poke_data_all:
      self.pokemons.append(poke_data[0])
    for pokemon in poke_data_all:
      print(pokemon)

  def get_all_pokemons(self, version) -> list:
    if version == PokemonData.RedGreen:
      return self.pokemons[:151]
    elif version == PokemonData.DiamondPearl:
      return self.pokemons[:494]
    elif version == PokemonData.SordShield:
      return self.pokemons[:900]


class PokemonWordler:
  wordle_data = []
  wordle_set = set()
  hits_dict = {}

  def __init__(self) -> None:
    pass

  def make_wordle_data(self, pokemon_list : list):
    for pokemon in pokemon_list:
      if len(pokemon) == 5:
        self.wordle_data.append(pokemon)
        self.wordle_set.add(pokemon)
        # 1文字ずつの辞書を作る
        for i in range(5):
          onechara = pokemon[i]
          if onechara not in self.hits_dict:
            self.hits_dict[onechara] = [set() for _ in range(5)]
          self.hits_dict[onechara][i].add(pokemon)
  
  def print_wordle_data(self):
    for pokemon in self.wordle_data:
      print(pokemon)
  
  def search(self, current_set : set, name : str, hitblow : str) -> set:
    if len(hitblow) != 5:
      return
    name_len = len(name)
    for i in range(name_len):
      # Color BLACK : character in BLACK position is NOT included
      if hitblow[i] == "b":
        for j in range(name_len):
          current_set -= self.hits_dict[name[i]][j]
      # Color YELLOW : includes character in YELLOW posision. And exclusive
      elif hitblow[i] == "y":
        tmp_set = set()
        for j in range(5): # hitblow len
          tmp_set |= self.hits_dict[name[i]][j]
        tmp_set -= self.hits_dict[name[i]][i]
        current_set &= tmp_set
      # Color GREEN :
      elif hitblow[i] == "g":
        current_set &= self.hits_dict[name[i]][i]
    return current_set

  def suggest(self, pokemon_list : list) -> list:
    poke_dict = {}
    # make dict
    for pokemon in pokemon_list:
      pokewords = list(set(list(pokemon)))
      for i in range(len(pokewords)):
        if pokewords[i] not in poke_dict:
          poke_dict[pokewords[i]] = 0
        poke_dict[pokewords[i]] += 1
    # calc score
    tmplist = []
    for pokemon in pokemon_list:
      score = 0
      pokewords = list(set(list(pokemon)))
      for i in range(len(pokewords)):
        score += poke_dict[pokewords[i]]
      tmplist.append([score, pokemon])
    tmplist.sort(reverse=True)
    result = [] # pokemon, score
    for score,name in tmplist:
      result.append([name, score])
    return result

if __name__ == "__main__":
  wordler = PokemonWordler()
  data = PokemonData()
  wordler.make_wordle_data(data.get_all_pokemons(version=PokemonData.SordShield))
  wset = wordler.wordle_set

  # print(wordler.suggest(list(wset)))

  # input and game
  while(True):
    poke, hitblow = input().split()
    wset = wordler.search(wset ,poke, hitblow)
    wlist = list(wset)
    candidate_list = wordler.suggest(wlist)
    print(candidate_list)

