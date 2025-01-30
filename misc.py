from PIL import Image
import os
import json

common_t_colors = [(255, 0, 255), (0, 255, 255), (255, 255, 0), (0, 0, 255), (255, 0, 0), (0, 255, 0)]

def get_t_color(colors):
    for i in range(len(common_t_colors)):
        if common_t_colors[i] not in colors:
            t_color_sub = common_t_colors[i]
            return t_color_sub, colors
    return None

def convert(input_path, output_path):
    try:
        t_needed = False
        t_color_sub = None
        image = Image.open(input_path).convert("RGBA")
        colors = [c[1] for c in image.convert("RGB").getcolors()]
        data = image.getdata()
        new_data = []
        for item in data:
            if item[3] == 0:
                if not t_needed:
                    t_needed = True
                    t_color_sub, colors = get_t_color(colors)
                new_data.append(t_color_sub)
            else:
                new_data.append(item)
        image.putdata(new_data)
        image.convert("RGB")
        image.save(output_path, format="BMP")
        print(f"Operation Complete: Transparency {t_needed}")
        return {"Finished": True, "Colors": colors, "Transparency?": t_needed, "Transparency Color": t_color_sub}
    except Exception as e:
        print(f"Operation Failed")
        return {"Finished": False, "Error": e}

def convert_all():
    try:
        rets = {}
        data = None
        with open("data.json", "r") as f:
            data = json.load(f)
            data["colors"] = {}
        pet = os.listdir("Pet")
        extra = os.listdir("Extras")
        backs = os.listdir("Backdrops")
        pngs = [f"Pet/{file[:-4]}" for file in pet if file.endswith(".png")] + [f"Extras/{file[:-4]}" for file in extra if file.endswith(".png")] + [f"Backdrops/{file[:-4]}" for file in backs if file.endswith(".png")]
        bmps = [f"Pet/{file}" for file in pet if file.endswith(".bmp")] + [f"Extras/{file}" for file in extra if file.endswith(".bmp")] + [f"Backdrops/{file}" for file in backs if file.endswith(".bmp")]
        for file in bmps:
            os.remove(file)
        for item in pngs:
            data["colors"][item] = {}
            ret = convert(f"{item}.png", f"{item}.bmp")
            if ret[2]:
                data["colors"][item]["colors"] = ret["Colors"]
                data["colors"][item]["t_color"] = ret["Transparency Color"]
            rets[item] = ret
        print("Operation Complete")
        with open("data.json", "w") as f:
            json.dump(obj=data, fp=f, indent=2)
        return rets
    except Exception as e:
        print(f"Operation Failed")
        return [False, e]

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
                ret = convert_all()
            else:
                ret = convert(inp[1], inp[2])
            if input("Show results? (y/n) ") == "y":
                print(ret)
        elif inp[0] == "show":
            print(show(inp[1], inp[2]))
        inp = input(">>> ")