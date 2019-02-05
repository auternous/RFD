import json

text = {'settings': {'scr_res': (800, 600), 'volume': 0.25,
                     'fullscreen': False},
        'screen_resolution':
            {"1920_1080":
                 {'objects':
                      {'player':
                           {'player_speed': 15
                            }}}}}
with open('Settings.json', 'w', encoding='utf-8') as f_obj:
    json.dump(text, f_obj, ensure_ascii=False)
with open('Settings.json', 'r', encoding='utf-8') as f_obj:
    a = json.load(f_obj)

print(a)
