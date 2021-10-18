
S = [
      [
        '.....',
        '.....',
        '..00.',
        '.00..',
        '.....'
      ],
      [   
        '.....',
        '..0..',
        '..00.',
        '...0.',
        '.....'
      ]
    ]

Z = [
      [
        '.....',
        '.....',
        '.00..',
        '..00.',
        '.....'
      ],
      [   
        '.....',
        '..0..',
        '.00..',
        '.0...',
        '.....'
      ]
    ]

I = [
      [
        '..0..',
        '..0..',
        '..0..',
        '..0..',
        '.....'
      ],
      [
        '.....',
        '0000.',
        '.....',
        '.....',
        '.....'
      ]
    ]

O = [
      [   
        '.....',
        '.....',
        '.00..',
        '.00..',
        '.....'
      ]
    ]

J = [
      [
        '.....',
        '.0...',
        '.000.',
        '.....',
        '.....'
      ],
      [
        '.....',
        '..00.',
        '..0..',
        '..0..',
        '.....'
      ],
      [
        '.....',
        '.....',
        '.000.',
        '...0.',
        '.....'
      ],
      [
        '.....',
        '..0..',
        '..0..',
        '.00..',
        '.....'
      ]
    ]

L = [
      [
        '.....',
        '...0.',
        '.000.',
        '.....',
        '.....'
      ],
      [
        '.....',
        '..0..',
        '..0..',
        '..00.',
        '.....'
      ],
      [
        '.....',
        '.....',
        '.000.',
        '.0...',
        '.....'
      ],
      [
        '.....',
        '.00..',
        '..0..',
        '..0..',
        '.....'
      ]
    ]

T = [
      [
        '.....',
        '..0..',
        '.000.',
        '.....',
        '.....'
      ],
      [
        '.....',
        '..0..',
        '..00.',
        '..0..',
        '.....'
      ],
      [
        '.....',
        '.....',
        '.000.',
        '..0..',
        '.....'
      ],
      [
        '.....',
        '..0..',
        '.00..',
        '..0..',
        '.....'
      ]
    ]

shapes = [S, Z, I, O, J, L, T]
#?_Gộp các khối vào mảng hính khối
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
#?_Theo thứ tự các khối trong hình khối thì sẽ có màu tương ứng


def convert_shape_format(shape): 
  positions = []
  format = shape.shape[shape.rotation % len(shape.shape)]

  for i, line in enumerate(format):
      row = list(line)
      for j, column in enumerate(row):
          if column == '0':
              positions.append((shape.x + j, shape.y + i))

  for i, pos in enumerate(positions):
      positions[i] = (pos[0] - 2, pos[1] - 4)

  return positions


def valid_space(shape, grid):
  accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
  accepted_pos = [j for sub in accepted_pos for j in sub]

  formatted = convert_shape_format(shape)

  for pos in formatted:
      if pos not in accepted_pos:
          if pos[1] > -1:
              return False
  return True
