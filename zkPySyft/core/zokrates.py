import os

#TODO: add comparison
MAP_INS_TO_DSL = {"add": "+", "mul": "*"}


class ZoKrates(object):
    def __init__(self, statements, inputs):
        self.code = []
        self.input_assign = []
        self.hasher_weights = 0
        self.hasher_data = 0

        #inject grounding statements

        for s in statements:
            res, lhs, rhs, ins = s
            z_ins = MAP_INS_TO_DSL[ins]
            l = '\tv{} = v{} {} v{}\n'.format(res, lhs, z_ins, rhs)
            self.code.append(l)

        self.header = 'def main('
        #inject grounding commit variables
        for input in inputs:
            self.input_assign.append(input['value'])

            # if ..
            #     if input['is_value']: update hasher1
            #     else : update_hasher2)

            if input['is_public']:
                self.header += 'field v{},'.format(input['index'])
            else:  #private
                self.header += 'private field v{},'.format(input['index'])

        self.header = self.header[:-1]  # delete trailing comma
        self.header += ') -> (field) \n\n'

    def compile(self, path):
        self.__write_code_file(path)
        self.path = path

    def __write_code_file(self, path):
        with open(path, "w+") as file:
            file.write(self.header)
            for l in self.code:
                file.write(l)

    def synthesize(self):
        cmd = './zokrates compile -i {}'.format(self.path)
        status = os.system(cmd)
        if __debug__:
            print(status)

    def setup(self):
        cmd = './zokrates setup'
        status = os.system(cmd)
        if __debug__:
            print(status)

    def compute_witness(self):
        #TODO: read args from file
        args = ' '.join(self.input_assign)
        cmd = './zokrates compute-witness -a {}'.format(args)
        status = os.system(cmd)
        if __debug__:
            print(status)

    def generate_proof(self):
        cmd = './zokrates generate-proof'
        status = os.system(cmd)
        if __debug__:
            print(status)

    def run(self, path):
        self.compile(path)
        self.synthesize()
        self.setup()
        self.compute_witness()
        self.generate_proof()
