from enum import Enum


class Mods:
    __slots__ = ('map_changing', 'nf', 'ez', 'hd', 'hr', 'dt', 'ht', 'nc',
                 'fl', 'so', 'speed_changing', 'map_changing')

    def __init__(self, mods_str=''):
        self.nf = False
        self.ez = False
        self.hd = False
        self.hr = False
        self.dt = False
        self.ht = False
        self.nc = False
        self.fl = False
        self.so = False
        self.speed_changing = False
        self.map_changing = False
        if mods_str:
            self.from_str(mods_str)
        self.update_state()

    def update_state(self):
        # speed changing - dt or ht or nc is used
        self.speed_changing = self.dt or self.ht or self.nc
        # if hr or ez or dt or ht or nc
        self.map_changing = self.hr or self.ez or self.speed_changing

    def __str__(self):
        string = ''
        if self.nf:
            string += "NF"
        if self.ez:
            string += "EZ"
        if self.hd:
            string += "HD"
        if self.hr:
            string += "HR"
        if self.dt:
            string += "DT"
        if self.ht:
            string += "HT"
        if self.nc:
            string += "NC"
        if self.fl:
            string += "FL"
        if self.so:
            string += "SO"
        return string

    def from_str(self, mods):
        if not mods:
            return
        # split mods string to chunks with length of two characters
        mods = [mods[i:i + 2] for i in range(0, len(mods), 2)]
        if "NF" in mods:
            self.nf = True
        if "EZ" in mods:
            self.ez = True
        if "HD" in mods:
            self.hd = True
        if "HR" in mods:
            self.hr = True
        if "DT" in mods:
            self.dt = True
        if "HT" in mods:
            self.ht = True
        if "NC" in mods:
            self.nc = True
        if "FL" in mods:
            self.fl = True
        if "SO" in mods:
            self.so = True
        self.update_state()


class AllMods(Enum):
    NoFail         = 1
    Easy           = 2
    TouchDevice    = 4
    Hidden         = 8
    HardRock       = 16
    SuddenDeath    = 32
    DoubleTime     = 64
    Relax          = 128
    HalfTime       = 256
    Nightcore      = 512 # Only set along with DoubleTime. i.e: NC only gives 576
    Flashlight     = 1024
    Autoplay       = 2048
    SpunOut        = 4096
    Relax2         = 8192 # Autopilot
    Perfect        = 16384 # Only set along with SuddenDeath. i.e: PF only gives 16416
    Key4           = 32768
    Key5           = 65536
    Key6           = 131072
    Key7           = 262144
    Key8           = 524288
    FadeIn         = 1048576
    Random         = 2097152
    Cinema         = 4194304
    Target         = 8388608
    Key9           = 16777216
    KeyCoop        = 33554432
    Key1           = 67108864
    Key3           = 134217728
    Key2           = 268435456
    ScoreV2        = 536870912
    LastMod        = 1073741824


def mod_list_to_val(mod_list):
    val = 0
    if mod_list is None:
        return val
    for mod in mod_list:
        val += mod.value
    return val


def val_to_mod_list(val):
    list = []
    iter = 0
    while(val > 0):
        is_enabled = val % 2
        if is_enabled == 1:
            list.append(AllMods(2 ** iter))
        val = val // 2
        iter += 1
    return list


def mod_list_to_string(mod_list):
    string = ""
    if mod_list is None:
        return string
    if AllMods.NoFail in mod_list:
        string += "NF"
    if AllMods.Easy in mod_list:
        string += "EZ"
    if AllMods.Hidden in mod_list:
        string += "HD"
    if AllMods.HardRock in mod_list:
        string += "HR"
    if AllMods.DoubleTime in mod_list:
        string += "DT"
    if AllMods.HalfTime in mod_list:
        string += "HT"
    if AllMods.Nightcore in mod_list:
        string += "NC"
        string.replace("DT", "")
    if AllMods.Flashlight in mod_list:
        string += "FL"
    if AllMods.SpunOut in mod_list:
        string += "SO"
    return string