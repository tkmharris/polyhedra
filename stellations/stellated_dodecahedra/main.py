import os.path
from stellated_dodecahedron_builder import StellatedDodecahedronBuilder

def generate_all_primitive_stellated_dodecahedra(path='stl', overwrite=False):
    primitive_stellated_dodecahedra_mappings = {
        'dodecahedron': ['base'],
        'small_stellated_dodecahedron': ['first_shell'],
        'great_dodecahedron': ['second_shell'],
        'great_stellated_dodecahedron': ['third_shell']
    }
    for name, regions in primitive_stellated_dodecahedra_mappings.items():
        print(f"Generating {name}...")
        mesh = StellatedDodecahedronBuilder.build_from_keys(regions)
        file = f"{path}/{name}.stl"
        if os.path.exists(file) and not overwrite:
            print(f"{file} exists, not overwriting")
            continue
        print(f"Writing {file}...")
        mesh.export(file)
    print("Done")

def main():
    generate_all_primitive_stellated_dodecahedra()

if __name__=='__main__':
    main()