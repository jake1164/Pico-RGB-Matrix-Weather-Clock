# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Jason Jackson
#
# SPDX-License-Identifier: MIT
"""
`jsoncreek`
================================================================================

Library for streaming a JSON requests api instead of using json.load()


* Author(s): Jason Jackson

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads


"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/jake1164/CircuitPython_JSONcreek.git"

from jsoncreek.visitor import visit, visit_items
__all__ = ["visit", "visit_items"]