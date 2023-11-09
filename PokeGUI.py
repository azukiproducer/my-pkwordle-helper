import tkinter as tk
from functools import partial
from PokemonWordler import PokemonWordler
from PokemonWordler import PokemonData

class PokeGUI():
  def __init__(self):
    self.root = tk.Tk()
    self.root.title("PokemonWordle Breaker")
    self.root.geometry("250x500")

    # configuration
    self.row_max = 10
    
    # member
    self.row = 0
    self.hitblow_buttons = []
    self.hitblow_texts = []
    self.current_suggestlistorder = 0
    self.suggestlist = []
    self.pokemon_list = tk.StringVar()

    # hit and blow button
    hitblow_frames = tk.Frame(self.root)
    for i in range(self.row_max):
      hitblow_frame = tk.Frame(hitblow_frames)
      for j in range(5):
        t = tk.StringVar(value=str("　"))
        bt = tk.Button(hitblow_frame,
          font=("",0,"bold"), # font=family[,size,weight,slant,under,overstrike]
          textvariable=t, fg="black", highlightbackground="white",
          command=partial(self.change_my_color, i*5+j))
        bt.pack(side=tk.LEFT)
        self.hitblow_buttons.append(bt)
        self.hitblow_texts.append(t)
      hitblow_frame.pack()
    hitblow_frames.pack()
    
    # Function button
    funcbutton_frame = tk.Frame(self.root)
    enter_button = tk.Button(funcbutton_frame, text="ENTER", command=self.on_enter_button)
    enter_button.pack(side=tk.RIGHT)
    clear_button = tk.Button(funcbutton_frame, text="CLEAR", command=self.on_clear_button)
    clear_button.pack(side=tk.LEFT)
    funcbutton_frame.pack()

    # Sort radiobutton
    sortradio_frame = tk.Frame(self.root)
    self.sortradio_score = tk.Radiobutton(sortradio_frame, variable=self.current_suggestlistorder, value=0, text="スコア順", command=self.on_scoresort_radiobutton)
    self.sortradio_score.pack(side=tk.LEFT)
    self.sortradio_name = tk.Radiobutton(sortradio_frame, variable=self.current_suggestlistorder, value=1, text="名前順", command=self.on_namesort_radiobutton)
    self.sortradio_name.pack(side=tk.RIGHT)
    sortradio_frame.pack()

    # Pokeom list
    pokelist_frame = tk.Frame(self.root)
    self.pokomon_listbox = tk.Listbox(pokelist_frame, listvariable=self.pokemon_list, height=10, highlightbackground="red")
    scrollbar = tk.Scrollbar(pokelist_frame, orient=tk.VERTICAL, command=self.pokomon_listbox.yview)
    self.pokomon_listbox["yscrollcommand"] = scrollbar.set
    self.pokomon_listbox.bind("<<ListboxSelect>>", lambda e: self.on_pokemon_selected())
    self.pokomon_listbox.pack()
    pokelist_frame.pack()

    # Main loop
    self.wordler = PokemonWordler()
    self.clear()
    self.root.mainloop()
  
  def clear(self):
    self.row = 0
    for i in range(self.row_max):
      for j in range(5):
        self.hitblow_texts[i*5+j].set("　")
        self.hitblow_buttons[i*5+j]["fg"] = "black"

    data = PokemonData()
    self.wordler.make_wordle_data(data.get_all_pokemons(version=PokemonData.SordShield))
    self.wset = self.wordler.wordle_set
    self.suggestlist = self.wordler.suggest(list(self.wset))
    self.set_pokemon_list(self.suggestlist)
    self.current_suggestlistorder = 0
    pass

  def on_enter_button(self) -> None:
    poke = self.get_hitblow_buttons_name(self.row)
    hitblow = ""
    for j in range(5):
      col = self.hitblow_buttons[self.row*5+j]["fg"]
      if col == "gray": c = "b"
      elif col == "orange": c = "y"
      elif col == "green": c = "g"
      else: return
      hitblow += (c)

    tmp_wset = self.wordler.search(self.wset ,poke, hitblow)
    if len(tmp_wset) != 0:
      self.wset = tmp_wset
      wlist = list(self.wset)
      self.suggestlist = self.wordler.suggest(wlist)
      self.set_pokemon_list(self.suggestlist)
      self.row += 1
      self.current_suggestlistorder = 0
    pass

  def on_clear_button(self):
    self.clear()

  def on_namesort_radiobutton(self):
    if self.current_suggestlistorder == 0:
      self.suggestlist.sort()
      self.set_pokemon_list(self.suggestlist)
      self.current_suggestlistorder = 1
    pass

  def on_scoresort_radiobutton(self):
    if self.current_suggestlistorder == 1:
      tmplist = []
      for x in self.suggestlist:
        tmplist.append([x[1], x[0]])
      tmplist.sort(reverse=True)
      dirlist = []
      for x in tmplist:
        dirlist.append([x[1], x[0]])
      self.set_pokemon_list(dirlist)
      self.suggestlist = dirlist
      self.current_suggestlistorder = 0
    pass
  
  def change_my_color(self, num):
    col = ""
    current = self.hitblow_buttons[num]["fg"]
    if current == "green" or current == "black":
      col = "gray"
    elif current == "gray":
      col = "orange"
    elif current == "orange":
      col = "green"
    self.hitblow_buttons[num]["fg"] = col
    pass

  def set_hitblow_buttons_name(self, name : str):
    for j in range(len(name)):
      self.hitblow_texts[self.row*5+j].set(name[j])
      self.hitblow_buttons[self.row*5+j]["fg"] = "black"
    pass

  def get_hitblow_buttons_name(self, row : int):
    name = ""
    for j in range(5):
      name += (self.hitblow_texts[row*5+j].get())
    return name

  def set_pokemon_list(self, pokemon_list): 
    self.pokemon_list.set(pokemon_list)

  def on_pokemon_selected(self):
    for i in self.pokomon_listbox.curselection():
      name, score = self.pokomon_listbox.get(i)
      break
    self.set_hitblow_buttons_name(name)
    pass

if __name__ == "__main__":
  app=PokeGUI()
