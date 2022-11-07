import numpy as np
import os


class ORCA_Data:
    def scan_table(self, word):
        # energy_scan
        try:
            with open(os.path.join(self.path, "orca.out")) as f:
                lines = f.readlines()

                data = []
                found_word = False

                for line in lines:
                    # check if string present on a current line
                    if line.find(word) != -1:
                        print(word, "string exists in file")
                        print("Line Number:", lines.index(line))
                        print("Line:", line)
                        found_word = True
                        continue

                    # Now we read lines until we encounter an empty line
                    if found_word:
                        if len(line.split()) > 1:
                            data.append([float(s) for s in line.split()])
                        else:
                            break
                return np.array(data)

        except FileNotFoundError:
            print("Could not open orca.out")
            return None

    def __init__(self, path):
        self.path = path
        self.atom_positions = []
        self.simple_input_line = []
        self.method = None
        self.basis = None
        self.energy_scan_actual = []
        self.energy_scan_minus_triple = []
        self.energy_scan_scf = []
        self.single_point_energies = []

        # atom positions
        try:
            with open(os.path.join(path, "orca.xyz")) as f:
                lines = f.readlines()
                for line in lines[2:]:
                    split = line.split()
                    self.atom_positions.append(
                        [split[0], np.array([float(s) for s in split[1:]])]
                    )
        except FileNotFoundError:
            print("Could not parse positions because orca.xyz was not found")

        # method and basis set
        try:
            with open(os.path.join(path, "orca.inp")) as f:
                lines = f.readlines()
                split = lines[0].split()

                self.simple_input_line = []
                for s in split:
                    self.simple_input_line.append(s)

                self.method = split[0][1:]
                self.basis = split[1]
        except FileNotFoundError:
            print("Could not method/basis because orca.inp was not found")

        # single point energies
        with open(os.path.join(self.path, "orca.out")) as f:
            word = "FINAL SINGLE POINT ENERGY"
            lines = f.readlines()
            for line in lines:
                # check if string present on a current line
                if line.find(word) != -1:
                    self.single_point_energies.append(float(line.split()[-1]))

        self.energy_scan_actual = self.scan_table("Actual Energy")
        self.energy_scan_scf = self.scan_table("Surface using the SCF energy")
        self.energy_scan_minus_triple = self.scan_table(
            "energy minus triple correction"
        )
