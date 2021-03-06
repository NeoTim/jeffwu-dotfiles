import os
import json

MOUSE_MODE_KEY = "semicolon"

ACTIVATE_TOGGLE = "m"
DOWN = "j"
UP = "k"
LEFT = "h"
RIGHT = "l"
FAST = "a"
SLOW = "s"
SCROLL = "d"
ARROW = "r"
LEFT_CLICK = "f"
MIDDLE_CLICK = "v"
RIGHT_CLICK = "g"
LEFT_CLICK_2 = "u"
MIDDLE_CLICK_2 = "i"
RIGHT_CLICK_2 = "o"

MOUSE_SCROLL_SPEED = 32
MOUSE_SPEED = 1200
MOUSE_SLOW_MULTIPLIER = 0.25
MOUSE_FAST_MULTIPLIER = 2

MOUSE_MODE = "jeffwu_mouse_mode"
# ARROW_MODE = "jeffwu_arrow_mode"
SCROLL_MODE = "jeffwu_scroll_mode"

SIMULTANEOUS_THRESHOLD_MS = 100

def var_is_set(var, value=1):
    """ Returns condition that variable is set. """
    return {
        "type": "variable_if",
        "name": var,
        "value": value
    }

def set_var(var, value=1):
    """ Returns condition that variable is set. """
    return {
        "set_variable": {
            "name": var,
            "value": value
        }
    }

def single_key(key_code, modifiers=[]):
    return {
        "key_code": key_code,
        "modifiers": {
            "mandatory": modifiers,
            "optional": [
                "any"
            ]
        }
    }

def simultaneous_keys(key_codes, after_up=None):
    res = {
        "simultaneous": [
            { "key_code": key_code } for key_code in key_codes
        ],
        "simultaneous_options": {
            "key_down_order": "strict",
            "key_up_order": "strict_inverse",
        },
        "modifiers": { "optional": [ "any" ] }
    }
    if after_up is not None:
        res["simultaneous_options"]["to_after_key_up"] = after_up
    return res

def basic_rule(items):
    return {
        "type": "basic",
        # "parameters": { "basic.simultaneous_threshold_milliseconds": SIMULTANEOUS_THRESHOLD_MS },
        **items
    }


def _scroll_combos(key):
    return [
        single_key(key, [ "left_shift" ]),
        single_key(key, [ "right_shift" ]),
        simultaneous_keys([SCROLL, key]),
    ]

def _toggle_combos():
    return [
        single_key(ACTIVATE_TOGGLE, ["left_command"]),
        single_key(ACTIVATE_TOGGLE, ["right_command"]),
        simultaneous_keys([MOUSE_MODE_KEY, ACTIVATE_TOGGLE]),
        # DONT KNOW WHY THIS DOESNT WORK
        simultaneous_keys(["escape", ACTIVATE_TOGGLE]),
    ]

# mouse_mode_rules = [
#     *[
#         basic_rule({
#             "from": fr,
#             "to": [ set_var(MOUSE_MODE, 0) ],
#             "conditions": [ var_is_set(MOUSE_MODE, 1) ]
#         }) for fr in [ single_key("escape"), single_key(MOUSE_MODE_KEY), single_key(ACTIVATE_TOGGLE) ]
#     ],
#     *[
#         basic_rule({
#             "from": fr,
#             "to": [
#                 set_var(MOUSE_MODE, 1),
#             ],
#             "conditions": [
#                 var_is_set(MOUSE_MODE, 0),
#             ],
#             "parameters": { "basic.simultaneous_threshold_milliseconds": SIMULTANEOUS_THRESHOLD_MS },
#         }) for fr in _toggle_combos()
#     ],
#     *[
#         basic_rule({
#             "from": fr,
#             "to": [
#                 set_var(MOUSE_MODE, 0),
#             ],
#             "conditions": [
#                 var_is_set(MOUSE_MODE, 1),
#             ],
#             "parameters": { "basic.simultaneous_threshold_milliseconds": SIMULTANEOUS_THRESHOLD_MS },
#         }) for fr in _toggle_combos()
#     ],
#     # NO-OP TO PREVENT WEIRD BEHAVIOR (sending d while scrolling)
#     basic_rule({
#         "from": single_key(UP),
#         "to": [
#             { "mouse_key": { "vertical_wheel": -MOUSE_SCROLL_SPEED } }
#         ],
#         "conditions": [
#             var_is_set(MOUSE_MODE),
#             var_is_set(SCROLL_MODE),
#         ]
#     }),
#     basic_rule({
#         "from": single_key(DOWN),
#         "to": [
#             { "mouse_key": { "vertical_wheel": MOUSE_SCROLL_SPEED } }
#         ],
#         "conditions": [
#             var_is_set(MOUSE_MODE),
#             var_is_set(SCROLL_MODE),
#         ]
#     }),
#     basic_rule({
#         "from": single_key(RIGHT),
#         "to": [
#             { "mouse_key": { "horizontal_wheel": MOUSE_SCROLL_SPEED } }
#         ],
#         "conditions": [
#             var_is_set(MOUSE_MODE),
#             var_is_set(SCROLL_MODE),
#         ]
#     }),
#     basic_rule({
#         "from": single_key(LEFT),
#         "to": [
#             { "mouse_key": { "horizontal_wheel": -MOUSE_SCROLL_SPEED } }
#         ],
#         "conditions": [
#             var_is_set(MOUSE_MODE),
#             var_is_set(SCROLL_MODE),
#         ]
#     }),
#     *[
#         basic_rule({
#             "from": fr,
#             "to": [
#                 { "mouse_key": { "vertical_wheel": -MOUSE_SCROLL_SPEED } }
#             ],
#             "conditions": [
#                 var_is_set(MOUSE_MODE),
#             ]
#         }) for fr in _scroll_combos(UP)
#     ],
#     *[
#         basic_rule({
#             "from": fr,
#             "to": [
#                 { "mouse_key": { "vertical_wheel": MOUSE_SCROLL_SPEED } }
#             ],
#             "conditions": [
#                 var_is_set(MOUSE_MODE),
#             ]
#         }) for fr in _scroll_combos(DOWN)
#     ],
#     *[
#         basic_rule({
#             "from": fr,
#             "to": [
#                 { "mouse_key": { "horizontal_wheel": MOUSE_SCROLL_SPEED } }
#             ],
#             "conditions": [
#                 var_is_set(MOUSE_MODE),
#             ]
#         }) for fr in _scroll_combos(RIGHT)
#     ],
#     *[
#         basic_rule({
#             "from": fr,
#             "to": [
#                 { "mouse_key": { "horizontal_wheel": -MOUSE_SCROLL_SPEED } }
#             ],
#             "conditions": [
#                 var_is_set(MOUSE_MODE),
#             ]
#         }) for fr in _scroll_combos(LEFT)
#     ],
#     basic_rule({
#         "from": single_key(SCROLL),
#         "to": [
#             set_var(MOUSE_MODE, 1),
#             set_var(SCROLL_MODE, 1),
#         ],
#         "to_after_key_up": [ set_var(SCROLL_MODE, 0) ],
#         "conditions": [
#             var_is_set(MOUSE_MODE, 1),
#         ]
#     }),
#     basic_rule({
#       "from": single_key(DOWN),
#       "to": [
#           { "mouse_key": { "y": MOUSE_SPEED } }
#       ],
#       "conditions": [
#           var_is_set(MOUSE_MODE),
#       ]
#     }),
#     basic_rule({
#       "from": single_key(UP),
#       "to": [
#           { "mouse_key": { "y": -MOUSE_SPEED } }
#       ],
#       "conditions": [
#           var_is_set(MOUSE_MODE),
#       ]
#     }),
#     basic_rule({
#       "from": single_key(LEFT),
#       "to": [
#           { "mouse_key": { "x": -MOUSE_SPEED } }
#       ],
#       "conditions": [
#           var_is_set(MOUSE_MODE),
#       ]
#     }),
#     basic_rule({
#       "from": single_key(RIGHT),
#       "to": [
#           { "mouse_key": { "x": MOUSE_SPEED } }
#       ],
#       "conditions": [
#           var_is_set(MOUSE_MODE),
#       ]
#     }),
#     *[
#         basic_rule({
#             "from": f,
#             "to": [
#                 { "pointing_button": "button1" }
#             ],
#             "conditions": [
#                 var_is_set(MOUSE_MODE),
#             ]
#         }) for f in [single_key(LEFT_CLICK), single_key(LEFT_CLICK_2)]
#     ],
#     *[
#         basic_rule({
#             "from": f,
#             "to": [
#                 { "pointing_button": "button3" }
#             ],
#             "conditions": [
#                 var_is_set(MOUSE_MODE),
#             ]
#         }) for f in [single_key(MIDDLE_CLICK), single_key(MIDDLE_CLICK_2)]
#     ],
#     *[
#         basic_rule({
#             "from": f,
#             "to": [
#                 { "pointing_button": "button2" }
#             ],
#             "conditions": [
#                 var_is_set(MOUSE_MODE),
#             ]
#         }) for f in [single_key(RIGHT_CLICK), single_key(RIGHT_CLICK_2), single_key(LEFT_CLICK, ["left_shift"]), single_key(LEFT_CLICK, ["right_shift"])]
#     ],
#     basic_rule({
#         "from": single_key(SLOW),
#         "to": [
#             { "mouse_key": { "speed_multiplier": MOUSE_SLOW_MULTIPLIER } }
#         ],
#         "conditions": [
#             var_is_set(MOUSE_MODE),
#         ]
#     }),
#     basic_rule({
#         "from": single_key(FAST),
#         "to": [
#             { "mouse_key": { "speed_multiplier": MOUSE_FAST_MULTIPLIER } }
#         ],
#         "conditions": [
#             var_is_set(MOUSE_MODE),
#         ]
#     }),
# ]

caps_lock_rules = [
    basic_rule({
        "from": single_key("caps_lock"),
        "to": [ { "key_code": "left_control" } ],
        "to_if_alone": [ { "key_code": "escape" } ],
    })
]

# NOTE: this is disabled because escape delay is too annoying
# Doing this with a simple rule instead
# right_command_rules = [
#     basic_rule({
#         "from": single_key("right_command"),
#         "to": [ { "key_code": "right_command" } ],
#         "to_if_alone": [ { "key_code": "escape" } ],
#     })
# ]

shift_rules = [
    basic_rule({
        "from": { "key_code": "left_shift" },
        "to": [ { "key_code": "left_shift" } ],
        "to_if_alone": [
            {
                "key_code": "9",
                "modifiers": [ "left_shift" ]
            }
        ]
    }),
    basic_rule({
        "from": { "key_code": "right_shift" },
        "to": [ { "key_code": "right_shift" } ],
        "to_if_alone": [
            {
                "key_code": "0",
                "modifiers": [ "right_shift" ]
            }
        ]
    }),
    # rolls
    basic_rule({
        "from": {
            "key_code": "left_shift",
            "modifiers": {
                "mandatory": [ "right_shift" ]
            }
        },
        "to": [
            { "key_code": "left_shift" },
            { "key_code": "right_shift" }
        ],
        "to_if_alone": [
            {
                "key_code": "0",
                # why both?
                "modifiers": [ "right_shift", "left_shift" ]
            },
            {
                "key_code": "9",
                "modifiers": [ "right_shift", "left_shift" ]
            }
        ]
    }),
    basic_rule({
        "from": {
            "key_code": "right_shift",
            "modifiers": {
                "mandatory": [ "left_shift" ]
            }
        },
        "to": [
            { "key_code": "right_shift" },
            { "key_code": "left_shift" }
        ],
        "to_if_alone": [
            {
                "key_code": "9",
                "modifiers": [ "right_shift" ]
            },
            {
                "key_code": "0",
                "modifiers": [ "right_shift" ]
            }
        ]
    })
]

# TODO: make it so holding works
# arrow_rules = [
#     basic_rule({
#         "from": simultaneous_keys([ARROW, LEFT], after_up=[set_var(ARROW_MODE, 0)]),
#         "to": [ { "key_code": "left_arrow" }, set_var(ARROW_MODE, 1) ],
#         "parameters": { "basic.simultaneous_threshold_milliseconds": SIMULTANEOUS_THRESHOLD_MS },
#     }),
#     basic_rule({
#         "from": simultaneous_keys([ARROW, DOWN], after_up=[set_var(ARROW_MODE, 0)]),
#         "to": [ { "key_code": "down_arrow" }, set_var(ARROW_MODE, 1) ],
#         "parameters": { "basic.simultaneous_threshold_milliseconds": SIMULTANEOUS_THRESHOLD_MS },
#     }),
#     basic_rule({
#         "from": simultaneous_keys([ARROW, RIGHT], after_up=[set_var(ARROW_MODE, 0)]),
#         "to": [ { "key_code": "right_arrow" }, set_var(ARROW_MODE, 1) ],
#         "parameters": { "basic.simultaneous_threshold_milliseconds": SIMULTANEOUS_THRESHOLD_MS },
#     }),
#     basic_rule({
#         "from": simultaneous_keys([ARROW, UP], after_up=[set_var(ARROW_MODE, 0)]),
#         "to": [ { "key_code": "up_arrow" }, set_var(ARROW_MODE, 1) ],
#         "parameters": { "basic.simultaneous_threshold_milliseconds": SIMULTANEOUS_THRESHOLD_MS },
#     }),
#     basic_rule({
#         "from": single_key(LEFT),
#         "to": [ { "key_code": "left_arrow" } ],
#         "conditions": [ var_is_set(ARROW_MODE), ]
#     }),
#     basic_rule({
#         "from": single_key(DOWN),
#         "to": [ { "key_code": "down_arrow" } ],
#         "conditions": [ var_is_set(ARROW_MODE), ]
#     }),
#     basic_rule({
#         "from": single_key(RIGHT),
#         "to": [ { "key_code": "right_arrow" } ],
#         "conditions": [ var_is_set(ARROW_MODE), ]
#     }),
#     basic_rule({
#         "from": single_key(UP),
#         "to": [ { "key_code": "up_arrow" } ],
#         "conditions": [ var_is_set(ARROW_MODE), ]
#     }),
# ]

SIMULTANEOUS_THRESHOLD_MS = 100
SIMULTANEOUS_THRESHOLD_MS_RULE = { "basic.simultaneous_threshold_milliseconds": SIMULTANEOUS_THRESHOLD_MS }

MOUSE_KEYS_MOUSE_MODE = "mouse_keys_mode"
MOUSE_KEYS_SCROLL_MODE = "mouse_keys_mode_scroll"
MOUSE_KEYS_ARROW_MODE = "mouse_keys_mode_arrows"

MOUSE_KEYS_AFTER_UP = [
    set_var(MOUSE_KEYS_MOUSE_MODE, 0),
    set_var(MOUSE_KEYS_SCROLL_MODE, 0),
    set_var(MOUSE_KEYS_ARROW_MODE, 0),
]

mouse_keys_rules = [
    basic_rule({
      "from": single_key(DOWN),
      "to": [
        { "mouse_key": { "vertical_wheel": 32 } }
      ],
      "conditions": [
        var_is_set(MOUSE_KEYS_MOUSE_MODE),
        var_is_set(MOUSE_KEYS_SCROLL_MODE),
      ]
    }),
    basic_rule({
      "from": single_key(DOWN),
      "to": [
        { "key_code": "down_arrow" }
      ],
      "conditions": [
        var_is_set(MOUSE_KEYS_MOUSE_MODE),
        var_is_set(MOUSE_KEYS_ARROW_MODE),
      ]
    }),
    basic_rule({
      "from": single_key(DOWN),
      "to": [
        { "mouse_key": { "y": MOUSE_SPEED } }
      ],
      "conditions": [
        var_is_set(MOUSE_KEYS_MOUSE_MODE),
      ]
    }),
    basic_rule({
        "from": simultaneous_keys([MOUSE_MODE_KEY, DOWN], after_up=MOUSE_KEYS_AFTER_UP),
        "to": [
            set_var(MOUSE_KEYS_MOUSE_MODE, 1),
            { "mouse_key": { "y": MOUSE_SPEED } }
        ],
        "parameters": SIMULTANEOUS_THRESHOLD_MS_RULE
    }),
    basic_rule({
        "from": single_key(UP),
        "to": [
            { "mouse_key": { "vertical_wheel": -MOUSE_SCROLL_SPEED } }
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
            var_is_set(MOUSE_KEYS_SCROLL_MODE),
        ]
    }),
    basic_rule({
        "from": single_key(UP),
        "to": [
            { "key_code": "up_arrow" }
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
            var_is_set(MOUSE_KEYS_ARROW_MODE),
        ]
    }),
    basic_rule({
        "from": single_key(UP),
        "to": [
            { "mouse_key": { "y": -MOUSE_SPEED } }
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
        ]
    }),
    basic_rule({
        "from": simultaneous_keys([MOUSE_MODE_KEY, UP], after_up=MOUSE_KEYS_AFTER_UP),
        "to": [
            set_var(MOUSE_KEYS_MOUSE_MODE, 1),
            { "mouse_key": { "y": -MOUSE_SPEED } }
        ],
        "parameters": SIMULTANEOUS_THRESHOLD_MS_RULE
    }),
    basic_rule({
        "from": single_key(LEFT),
        "to": [
            { "mouse_key": { "horizontal_wheel": MOUSE_SCROLL_SPEED } }
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
            var_is_set(MOUSE_KEYS_SCROLL_MODE),
        ]
    }),
    basic_rule({
        "from": single_key(LEFT),
        "to": [
            { "key_code": "left_arrow" }
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
            var_is_set(MOUSE_KEYS_ARROW_MODE),
        ]
    }),
    basic_rule({
        "from": single_key(LEFT),
        "to": [
            { "mouse_key": { "x": -MOUSE_SPEED } }
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
        ]
    }),
    basic_rule({
        "from": simultaneous_keys([MOUSE_MODE_KEY, LEFT], after_up=MOUSE_KEYS_AFTER_UP),
        "to": [
            set_var(MOUSE_KEYS_MOUSE_MODE, 1),
            { "mouse_key": { "x": -MOUSE_SPEED } }
        ],
        "parameters": SIMULTANEOUS_THRESHOLD_MS_RULE
    }),
    basic_rule({
        "from": single_key(RIGHT),
        "to": [
            { "mouse_key": { "horizontal_wheel": -MOUSE_SCROLL_SPEED } }
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
            var_is_set(MOUSE_KEYS_SCROLL_MODE),
        ]
    }),
    basic_rule({
        "from": single_key(RIGHT),
        "to": [
            { "key_code": "right_arrow" }
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
            var_is_set(MOUSE_KEYS_ARROW_MODE),
        ]
    }),
    basic_rule({
        "from": single_key(RIGHT),
        "to": [
            { "mouse_key": { "x": MOUSE_SPEED } }
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
        ]
    }),
    basic_rule({
        "from": simultaneous_keys([MOUSE_MODE_KEY, RIGHT], after_up=MOUSE_KEYS_AFTER_UP),
        "to": [
            set_var(MOUSE_KEYS_MOUSE_MODE, 1),
            { "mouse_key": { "x": MOUSE_SPEED } }
        ],
        "parameters": SIMULTANEOUS_THRESHOLD_MS_RULE
    }),
    basic_rule({
        "from": single_key(LEFT_CLICK),
        "to": [
            { "pointing_button": "button1" }
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
        ]
    }),
    basic_rule({
        "from": simultaneous_keys([MOUSE_MODE_KEY, LEFT_CLICK], after_up=MOUSE_KEYS_AFTER_UP),
        "to": [
            set_var(MOUSE_KEYS_MOUSE_MODE, 1),
            { "pointing_button": "button1" }
        ],
        "parameters": SIMULTANEOUS_THRESHOLD_MS_RULE
    }),
    basic_rule({
        "from": single_key(MIDDLE_CLICK),
        "to": [
            { "pointing_button": "button3" }
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
        ]
    }),
    basic_rule({
        "from": simultaneous_keys([MOUSE_MODE_KEY, MIDDLE_CLICK], after_up=MOUSE_KEYS_AFTER_UP),
        "to": [
            set_var(MOUSE_KEYS_MOUSE_MODE, 1),
            { "pointing_button": "button3" }
        ],
        "parameters": SIMULTANEOUS_THRESHOLD_MS_RULE
    }),
    basic_rule({
        "from": single_key(RIGHT_CLICK),
        "to": [
            { "pointing_button": "button2" }
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
        ]
    }),
    basic_rule({
        "from": simultaneous_keys([MOUSE_MODE_KEY, RIGHT_CLICK], after_up=MOUSE_KEYS_AFTER_UP),
        "to": [
            set_var(MOUSE_KEYS_MOUSE_MODE, 1),
            { "pointing_button": "button2" }
        ],
        "parameters": SIMULTANEOUS_THRESHOLD_MS_RULE
    }),
    basic_rule({
        "from": single_key(SCROLL),
        "to": [
            set_var(MOUSE_KEYS_SCROLL_MODE, 1),
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
        ],
        "to_after_key_up": [
            set_var(MOUSE_KEYS_SCROLL_MODE, 0),
        ]
    }),
    basic_rule({
        "from": simultaneous_keys([MOUSE_MODE_KEY, SCROLL], after_up=MOUSE_KEYS_AFTER_UP),
        "to": [
            set_var(MOUSE_KEYS_MOUSE_MODE, 1),
            set_var(MOUSE_KEYS_SCROLL_MODE, 1),
        ],
        "parameters": SIMULTANEOUS_THRESHOLD_MS_RULE,
        "to_after_key_up": [
            set_var(MOUSE_KEYS_SCROLL_MODE, 0),
        ]
    }),
    basic_rule({
        "from": single_key(FAST),
        "to": [
            { "mouse_key": { "speed_multiplier": MOUSE_FAST_MULTIPLIER } }
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
        ]
    }),
    basic_rule({
        "from": simultaneous_keys([MOUSE_MODE_KEY, FAST], after_up=MOUSE_KEYS_AFTER_UP),
        "to": [
            set_var(MOUSE_KEYS_MOUSE_MODE, 1),
            { "mouse_key": { "speed_multiplier": MOUSE_FAST_MULTIPLIER } }
        ],
        "parameters": SIMULTANEOUS_THRESHOLD_MS_RULE
    }),
    basic_rule({
        "from": single_key(SLOW),
        "to": [
            { "mouse_key": { "speed_multiplier": MOUSE_SLOW_MULTIPLIER } }
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
        ]
    }),
    basic_rule({
        "from": simultaneous_keys([MOUSE_MODE_KEY, SLOW], after_up=MOUSE_KEYS_AFTER_UP),
        "to": [
            set_var(MOUSE_KEYS_MOUSE_MODE, 1),
            { "mouse_key": { "speed_multiplier": MOUSE_SLOW_MULTIPLIER } }
        ],
        "parameters": SIMULTANEOUS_THRESHOLD_MS_RULE
    }),
    basic_rule({
        "from": single_key(ARROW),
        "to": [
            set_var(MOUSE_KEYS_ARROW_MODE, 1),
        ],
        "conditions": [
            var_is_set(MOUSE_KEYS_MOUSE_MODE),
        ],
        "to_after_key_up": [
            set_var(MOUSE_KEYS_ARROW_MODE, 0),
        ]
    }),
    basic_rule({
        "from": simultaneous_keys([MOUSE_MODE_KEY, ARROW], after_up=MOUSE_KEYS_AFTER_UP),
        "to": [
            set_var(MOUSE_KEYS_MOUSE_MODE, 1),
            set_var(MOUSE_KEYS_ARROW_MODE, 1),
        ],
        "parameters": SIMULTANEOUS_THRESHOLD_MS_RULE,
        "to_after_key_up": [
            set_var(MOUSE_KEYS_SCROLL_MODE, 0),
        ]
    })
]


with open(os.path.realpath(__file__).replace('.py', '.json'), 'w') as f:
    json.dump({
        "title": "Jeff Wu's karabiner settings",
        "rules": [
            # {
            #     "description": "Mouse Mode",
            #     "manipulators": mouse_mode_rules,
            # },
            {
                "description": "Mouse Keys",
                "manipulators": mouse_keys_rules,
            },
            {
                "description": "Caps Lock to Control, Escape on single press.",
                "manipulators": caps_lock_rules,
            },
            # {
            #     "description": "Right Command to Escape.",
            #     "manipulators": right_command_rules,
            # },
            # {
            #     "description": "semicolon = arrows",
            #     "manipulators": arrow_rules,
            # },
            {
                "description": "Better Shifting: Parentheses on shift keys",
                "manipulators": shift_rules,
            },
            {
                "description": "Change caps + space to backspace",
                "manipulators": [
                    basic_rule({
                        # use left control since we map caps to that
                        "from": single_key("spacebar", [ "left_control" ]),
                        "to": [ { "key_code": "delete_or_backspace" } ],
                    }),
                ]
            }
    ],
    }, f, indent=2)


