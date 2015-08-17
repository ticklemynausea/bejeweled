# -*- coding: utf-8 -*-

import random
import os

def colored(text, color = None, background = None, attributes = None):

    COLORS = {
      1 : 31,
      2 : 34,
      3 : 32,
      4 : 33,
      5 : 36,
      6 : 35,
      7 : 37,
      8 : 137,
    }

    HIGHLIGHTS = {
      1 : 41,
      2 : 44,
      3 : 42,
      4 : 43,
      5 : 46,
      6 : 45,
      7 : 47,
    }

    ATTRIBUTES = {
           'bold' : 1,
           'dark' : 2,
               '' : 3,
       'underline': 4,
          'blink' : 5,
               '' : 6,
        'reverse' : 7,
      'concealed' : 8
    }


    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'

        if color is not None:
            text = fmt_str % (COLORS[color], text)

        if background is not None:
            text = fmt_str % (HIGHLIGHTS[background], text)

        if attributes is not None:
            for attr in attributes:
                text = fmt_str % (ATTRIBUTES[attr], text)

        text += '\033[0m'

    return text


class Matrix(object):

    __slots__ = [
      'cols', 'rows', 'matrix'
    ]

    @staticmethod
    def CopyMatrix(matrix):
        cols = len(matrix[0])
        rows = len(matrix)
        m = Matrix(cols, rows)

        for i in range(rows):
            for j in range(cols):
                m.matrix[i][j] = matrix[i][j]

        return m

    def __init__(self, cols, rows, colors = None):
        self.cols = cols
        self.rows = rows
        self.matrix = [[0] * cols for _ in range(0, rows)]

        if colors is not None:
            for i in range(rows):
                for j in range(cols):
                    self.matrix[i][j] = random.choice(range(1, colors+1))

    def __repr__(self):
        return self.reprConsole()

    def setItem(self, col, row, v):
        self.matrix[col][row] = v

    def getItem(self, col, row):
        return self.matrix[col][row]

    def reprConsole(self):
        outStr = ""

        outStr += "    "
        for i in range(0, self.cols):
            outStr += "%s " % (i % 10)
        outStr += "\n"

        for i in range(self.rows-1, -1, -1):
            outStr += "%s [" % (i % 10)
            l = len(self.matrix[i])
            for j in range(l):
                c = self.matrix[i][j]
                if c == 0:
                    outStr += "  "
                else:
                    outStr += colored("%s " % c, c, c)

            outStr += "] %s\n" % (i % 10)
        outStr += "    "
        for i in range(0, self.cols):
            outStr += "%s " % (i % 10)
        outStr += "\n"
        return outStr

    def reprConsoleMarkMoves(self, moves):

        markers = [[0] * self.cols for _ in range(0, self.rows)]

        for move in moves:
            coord_x1 = move[1]
            coord_y1 = move[0]

            markers[coord_y1][coord_x1] = 1

        outStr = ""
        for i in range(self.rows-1, -1, -1):
            outStr += "%s [" % i
            l = len(self.matrix[i])
            for j in range(l):
                c = self.matrix[i][j]
                if markers[i][j] == 1:
                    if c == 0:
                        outStr += "!!"
                    else:
                        outStr += colored("!!", 7, c, ['bold'])
                else:
                    if c == 0:
                        outStr += "  "
                    else:
                        outStr += colored("%s " % c, c, c)
            outStr += "]\n"

        outStr += "   "
        for i in range(0, self.cols):
            outStr += "%s " % i
        outStr += "\n"

        return outStr
