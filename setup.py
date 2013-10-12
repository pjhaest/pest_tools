#! /usr/bin/env python

from distutils.core import setup

DESCRIPTION = """\
Python modules used to aid in model calibration with PEST (Doherty, 2010)

Main goal is for quick development of visuals on important PEST ouput.

Reference
---------
Doherty, J., 2010, PEST, Model-independent parameter estimation—User 
manual, 5th ed.: Brisbane, Australia, Watermark Numerical Computing.

"""

def run():
    setup(name="PestTools",
        version="0.1",
        description="Tools to aid in model calibration wtih PEST",
        url="",
        license="MIT",
        author="Evan Christianson",
        maintainer_email="",
        packages=["pest_tools"],
        long_description=DESCRIPTION,
    )

if __name__ == "__main__":
    run()


