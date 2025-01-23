from PIL import Image

def convert(input_path, output_path):
    try:
        image = Image.open(input_path).convert("RGBA")
        image.save(output_path, format="BMP", bitmap_format="BMP;32")
        return "Operation Successful"
    except Exception as e:
        return f"Operation Failed: {e}"

def show (input_path, output_path):
    try:
        image = Image.open(input_path)
        width, height = image.size
        pixels = list(image.getdata())

        with open(output_path, 'w') as file:
            file.write(f"Width: {width}\n")
            file.write(f"Height: {height}\n")
            file.write("Pixels:\n")
            for y in range(height):
                for x in range(width):
                    file.write(f"{pixels[y * width + x]} ")
                file.write("\n")
        return "Operation Successful"
    except Exception as e:
        return f"Operation Failed: {e}"

if __name__ == "__main__":
    inp = input(">>> ")
    while inp != "exit":
        inp = inp.split(" ")
        if inp[0] == "convert":
            print(convert(inp[1], inp[2]))
        elif inp[0] == "show":
            print(show(inp[1], inp[2]))
        inp = input(">>> ")