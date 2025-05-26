import random

LEVEL_CONFIG = {
        "floor_segments": [
            {
                'x_start': 0, 
                'x_end': 3,
                'y_level': 0,  # 1 блок от низа экрана
                'layers': 3
            },
            {
                'x_start': 5,
                'x_end': 5,
                'y_level': 0,  # на 2 блока выше основного пола
                'layers': 3
            },
            {
                'x_start': 6,
                'x_end': 8,
                'y_level': 0,  # на 2 блока выше основного пола
                'layers': 4
            },
            {
                'x_start': 10,
                'x_end': 10,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 11,
                'x_end': 12,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 13,
                'x_end': 13,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 14,
                'x_end': 16,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 17,
                'x_end': 17,
                'y_level': 0,
                'layers': 5
            },
            {
                'x_start': 18,
                'x_end': 20,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 22,
                'x_end': 22,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 24,
                'x_end': 26,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 27,
                'x_end': 27,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 29,
                'x_end': 29,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 31,
                'x_end': 33,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 34,
                'x_end': 35,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 37,
                'x_end': 37,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 39,
                'x_end': 39,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 40,
                'x_end': 45,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 46,
                'x_end': 47,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 48,
                'x_end': 50,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 49,
                'x_end': 49,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 51,
                'x_end': 52,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 54,
                'x_end': 54,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 56,
                'x_end': 56,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 57,
                'x_end': 63,
                'y_level': 0,
                'layers': 3
            },

            {
                'x_start': 58,
                'x_end': 59,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 64,
                'x_end': 64,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 65,
                'x_end': 69,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 68,
                'x_end': 73,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 74,
                'x_end': 74,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 75,
                'x_end': 79,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 78,
                'x_end': 78,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 81,
                'x_end': 81,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 83,
                'x_end': 86,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 87,
                'x_end': 89,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 89,
                'x_end': 93,
                'y_level': 8,
                'layers': 1
            },
            {
                'x_start': 90,
                'x_end': 94,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 95,
                'x_end': 98,
                'y_level': 0,
                'layers': 6
            },
            {
                'x_start': 99,
                'x_end': 100,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 102,
                'x_end': 103,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 104,
                'x_end': 104,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 104,
                'x_end': 113,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 107,
                'x_end': 108,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 109,
                'x_end': 113,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 111,
                'x_end': 113,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 115,
                'x_end': 116,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 114,
                'x_end': 124,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 120,
                'x_end': 122,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 123,
                'x_end': 124,
                'y_level': 5,
                'layers': 2
            },
            {
                'x_start': 121,
                'x_end': 123,
                'y_level': 7,
                'layers': 1
            },
            {
                'x_start': 125,
                'x_end': 127,
                'y_level': 0,
                'layers': 6
            },
            {
                'x_start': 128,
                'x_end': 130,
                'y_level': 0,
                'layers': 7
            },
            {
                'x_start': 131,
                'x_end': 132,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 133,
                'x_end': 142,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 133,
                'x_end': 135,
                'y_level': 7,
                'layers': 1
            },
            {
                'x_start': 137,
                'x_end': 139,
                'y_level': 8,
                'layers': 1
            },
            {
                'x_start': 141,
                'x_end': 142,
                'y_level': 7,
                'layers': 1
            },
            {
                'x_start': 144,
                'x_end': 146,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 144,
                'x_end': 144,
                'y_level': 7,
                'layers': 1
            },
            {
                'x_start': 146,
                'x_end': 148,
                'y_level': 7,
                'layers': 1
            },
            {
                'x_start': 147,
                'x_end': 149,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 150,
                'x_end': 150,
                'y_level': 0,
                'layers': 5
            },
            {
                'x_start': 151,
                'x_end': 153,
                'y_level': 0,
                'layers': 6
            },
            {
                'x_start': 154,
                'x_end': 154,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 155,
                'x_end': 156,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 157,
                'x_end': 159,
                'y_level': 0,
                'layers': 6
            },
            {
                'x_start': 160,
                'x_end': 162,
                'y_level': 0,
                'layers': 7
            },
            {
                'x_start': 163,
                'x_end': 165,
                'y_level': 0,
                'layers': 6
            },
            {
                'x_start': 166,
                'x_end': 167,
                'y_level': 0,
                'layers': 5
            },
            {
                'x_start': 168,
                'x_end': 179,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 170,
                'x_end': 170,
                'y_level': 7,
                'layers': 3
            },
            {
                'x_start': 171,
                'x_end': 172,
                'y_level': 9,
                'layers': 1
            },
            {
                'x_start': 171,
                'x_end': 172,
                'y_level': 7,
                'layers': 1
            },
            {
                'x_start': 172,
                'x_end': 173,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 172,
                'x_end': 172,
                'y_level': 3,
                'layers': 1
            },
            {
                'x_start': 174,
                'x_end': 177,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 175,
                'x_end': 176,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 179,
                'x_end': 179,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 181,
                'x_end': 182,
                'y_level': 7,
                'layers': 1
            },
            {
                'x_start': 181,
                'x_end': 186,
                'y_level': 3,
                'layers': 1
            },
            {
                'x_start': 187,
                'x_end': 189,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 190,
                'x_end': 195,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 197,
                'x_end': 198,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 201,
                'x_end': 207,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 203,
                'x_end': 205,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 209,
                'x_end': 211,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 212,
                'x_end': 213,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 213,
                'x_end': 217,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 219,
                'x_end': 221,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 222,
                'x_end': 222,
                'y_level': 0,
                'layers': 5
            },
            {
                'x_start': 224,
                'x_end': 227,
                'y_level': 0,
                'layers': 6
            },
            {
                'x_start': 228,
                'x_end': 230,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 228,
                'x_end': 228,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 228, #длинная
                'x_end': 240,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 233,
                'x_end': 238,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 240,
                'x_end': 242,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 244,
                'x_end': 245,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 243,
                'x_end': 254,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 245,
                'x_end': 245,
                'y_level': 3,
                'layers': 1
            },
            {
                'x_start': 246,
                'x_end': 249,
                'y_level': 3,
                'layers': 2
            },
            {
                'x_start': 247,
                'x_end': 249,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 250,
                'x_end': 254,
                'y_level': 3,
                'layers': 1
            },
            {
                'x_start': 251,
                'x_end': 257,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 256,
                'x_end': 258,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 259,
                'x_end': 262,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 263,
                'x_end': 266,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 268,
                'x_end': 271,
                'y_level': 3,
                'layers': 1
            },
            {
                'x_start': 272,
                'x_end': 275,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 277,
                'x_end': 284,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 285,
                'x_end': 288,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 289,
                'x_end': 290,
                'y_level': 0,
                'layers': 5
            },
            {
                'x_start': 291,
                'x_end': 293,
                'y_level': 0,
                'layers': 6
            },
        ],
        "strawberries": [
            (12, 2),
            (49, 2),
            (78, 5),
            (122, 5),
            (144, 7),
            (171, 7),
            (204, 5),
            (229, 2),
            (254, 3)
        ],
        "enemies": [
            (41, 2, 0.5, 0.7, random.randint(1, 5)),
            (74, 3, 0.5, 0.7, random.randint(1, 5)),
            (106, 2, 0.5, 0.7, random.randint(1, 5)),
            (119, 2, 0.5, 0.7, random.randint(1, 5)),
            (136, 2, 0.5, 0.7, random.randint(1, 5)),
            (183, 3, 0.5, 0.7, random.randint(1, 5)),
            (215, 2, 0.5, 0.7, random.randint(1, 5)),
            (234, 2, 0.5, 0.7, random.randint(1, 5)),
            (281, 2, 0.5, 0.7, random.randint(1, 5))
        ]
    }

