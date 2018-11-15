
available_states = [

    {
        "name": "mono",
        "state": {
            "grating": [1, 2],
            "wavelength": list(range(250, 1000)),
        }
    },

    {
        "name": "lpfw",
        "state": {
            "position": list(range(1, 7)),
            "sensors": [0, 1],
        }
    },

    {
        "name": "spfw",
        "state": {
            "position":  list(range(1, 7)),
            "sensors": [0, 1],
         }
    },

    {
        "name": "source",
        "state": {
            "power": [round(x/2, 1) for x in range(60, 201)],
        }
    },

    {
        "name": "flipper",
        "state": {
            "position": ["up", "down"],
        }
    },

    {
        "name": "crystal_wheel",
        "state": {
            "position": list(range(1, 13)),
            # "speed": list(),
        }
    },

]

base_measurements = [
    {
        "name": "Andor",
        "config": {
            "exposure": 10,
            "pre_amp_gain": 4,
            "grating": 2,
            "center_wavelength": 500,
            "slit_width": 1000,
        }

    },

    {
        "name": "PowerMeter",
        "config": {
            "samples_per_sec": 100,
            "avg_every": 100,
        }
    }
]
