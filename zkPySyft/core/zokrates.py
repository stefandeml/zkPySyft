import os


class ZoKrates:
    def __init__(self, instructions, inputs_and_outputs):
        self.code = []
        self.input_assignments = []
        self.outputs = []
        self.gadgets = []
        self.gadget_assignments = {}

        self.header = ["def main("]
        # Array for storing the parameters of the main method
        parameters = []
        for entry in inputs_and_outputs:
            if entry["is_input"]:
                # FIXME: assert that all values in pysyft input file are set
                self.input_assignments.append(entry["value"])

                if entry["is_public"]:
                    parameters.append("field v{}".format(entry["index"]))
                else:  # private
                    parameters.append("private field v{}".format(entry["index"]))
            else:
                self.outputs.append("v{}".format(entry["index"]))

        self.header.append(", ".join(parameters))

        # Data-grounding
        #TODO: fix import using PyPI later
        from depends.pycrypto.zokrates.gadgets.pedersenHasher import PedersenHasher
        hasher = PedersenHasher("allInputsHasher")
        self.gadgets.append(hasher)
        inputs_hash_digest = hasher.hash_scalars(*(int(i) for i in self.input_assignments))
        self.gadget_assignments[hasher] = hasher.gen_dsl_witness_scalars(*(int(i) for i in self.input_assignments)) 
        self.header.append(", field[{}] inputsHashBits".format(hasher.segments*3))

        self.header.append(") -> (field): \n\n")
        self.header = "".join(self.header)

        for ins in instructions:
            # Add indentation and newline to each line in the code block
            self.code.append("\t{}\n".format(ins.to_zokrates()))
        

        self.code.append("\tfield[2] inputsHashDigest = {name}(inputsHashBits)\n".format(name=hasher.name))
        self.code.append("\t{} = inputsHashDigest[0]\n".format(inputs_hash_digest.x))
        self.code.append("\t{} = inputsHashDigest[1]\n".format(inputs_hash_digest.y))

        # Return the outputs
        if self.outputs:
            self.code.append("\treturn {}\n".format(",".join(self.outputs)))
        else:
            # Return 1 if no outputs are specified, as ZoKrates requires a
            # return statement
            self.code.append("\treturn 1\n")

    def compile(self, path):
        self.__write_code_file(path)
        if self.gadgets:
            self.__write_gadget_code_files()
        self.path = path

    def synthesize(self):
        cmd = "zokrates compile -i {}".format(self.path)
        status = os.system(cmd)
        if __debug__:
            print(status)

    def setup(self):
        cmd = "zokrates setup"
        status = os.system(cmd)
        if __debug__:
            print(status)

    def compute_witness(self):
        # TODO: read args from file
        args = " ".join(self.input_assignments)
        if self.gadgets:
           for g in self.gadgets:
               args += " ".join(self.gadget_assignments[g])
        cmd = "zokrates compute-witness -a {}".format(args)
        return cmd
        # status = os.system(cmd)
        # if __debug__:
        #     print(status)

    def generate_proof(self):
        cmd = "zokrates generate-proof"
        status = os.system(cmd)
        if __debug__:
            print(status)

    def run(self, path):
        self.compile(path)
        self.synthesize()
        self.setup()
        self.compute_witness()
        self.generate_proof()

    def __write_gadget_code_files(self):
        gadgets = self.gadgets
        for g in gadgets:
            with open(g.name + ".code", "w+") as f:
                f.write(g.dsl_code)

    def __write_code_file(self, path):
        with open(path, "w+") as f:
            # add imports to header
            if self.gadgets: 
                for g in self.gadgets:
                    self.header = "import \"{name}.code\" as {name} \n".format(name=g.name) + self.header

            f.write(self.header)
            for l in self.code:
                f.write(l)
