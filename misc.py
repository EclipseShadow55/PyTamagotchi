from PIL import Image
import os

def convert(input_path, output_path):
    try:
        image = Image.open(input_path).convert("RGBA")
        image.save(output_path, format="BMP", bitmap_format="BMP;32")
        data = image.getdata()
        new_data = []
        for item in data:
            if item[3] == 0:
                new_data.append((255, 0, 255,))
            else:
                new_data.append(item)
        image.putdata(new_data)
        image.convert("RGB")
        image.save(output_path, format="BMP")
        return "Operation Successful"
    except Exception as e:
        return f"Operation Failed: {e}"

def convertAll():
    try:
        pngs = os.listdir("PNGs")
        for i in range(len(pngs)):
            if not pngs[i].endswith(".png"):
                pngs.pop(i)
            else:
                pngs[i] = pngs[i][:-4]
        clear_directory("BMPs")
        for item in pngs:
            ret = convert(f"PNGs/{item}.png", f"BMPs/{item}.bmp")
            if ret != "Operation Successful":
                return ret
        return "Operation Successful"
    except Exception as e:
        return f"Operation Failed: {e}"

def clear_directory(directory_path):
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        os.remove(file_path)
    print("Directory cleared successfully.")

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
            if len(inp) < 3:
                print(convertAll())
            else:
                print(convert(inp[1], inp[2]))
        elif inp[0] == "show":
            print(show(inp[1], inp[2]))
        inp = input(">>> ")