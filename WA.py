import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk

# ============ CONFIG =============
API_KEY = "API_KEY"  # Replace this with your actual API key
ICON_PATHS = {
    "Clouds": "clouds.png",
    "Rain": "rain.png",
    "Drizzle": "drizzle.png",
    "Mist": "mist.png",
    "Snow": "snow.png",
    "Clear": "sun.png",       # You must add this manually
    "Wind": "wind.png"
}
DEFAULT_ICON = "clouds.png"
# ==================================

def get_weather(city):
    if not API_KEY or API_KEY == "your_openweathermap_api_key":
        messagebox.showerror("API Key Error", "Please enter a valid OpenWeatherMap API key.")
        return

    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            raise Exception(data.get("message", "Failed to get weather."))

        display_weather(data)

    except Exception as e:
        messagebox.showerror("Error", f"Could not retrieve weather data: {e}")

def display_weather(data):
    city = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"].title()
    condition = data["weather"][0]["main"]
    wind_speed = data["wind"]["speed"]

    label_location.config(text=f"{city}, {country}")
    label_temp.config(text=f"{temp:.1f} °C")
    label_desc.config(text=desc)
    label_wind.config(text=f"Wind Speed: {wind_speed} m/s")

    # Load icon
    icon_file = ICON_PATHS.get(condition, DEFAULT_ICON)
    try:
        img = Image.open(icon_file)
        img = img.resize((100, 100))
        icon_photo = ImageTk.PhotoImage(img)
        label_icon.config(image=icon_photo)
        label_icon.image = icon_photo
    except Exception:
        label_icon.config(text="(Icon missing)")

# ========== GUI ==============
root = tk.Tk()
root.title("Weather App")
root.geometry("350x450")
root.configure(bg="#e0f7fa")

style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Header
header = ttk.Label(frame, text="Weather App", style="Header.TLabel", foreground="#00796b")
header.pack(pady=10)

# Search icon beside entry
try:
    search_icon = Image.open("search.png").resize((20, 20), Image.ANTIALIAS)
    search_icon_tk = ImageTk.PhotoImage(search_icon)
    search_label = tk.Label(frame, image=search_icon_tk, bg="#e0f7fa")
    search_label.image = search_icon_tk
    search_label.place(x=40, y=65)
except Exception:
    pass

# Entry field
entry_city = ttk.Entry(frame, width=25)
entry_city.pack(pady=5)
entry_city.insert(0, "Enter city")

# Search button
ttk.Button(frame, text="Get Weather", command=lambda: get_weather(entry_city.get())).pack(pady=10)

# Weather display
label_icon = ttk.Label(frame)
label_icon.pack(pady=10)

label_location = ttk.Label(frame, text="", font=("Segoe UI", 12))
label_location.pack()

label_temp = ttk.Label(frame, text="", font=("Segoe UI", 12))
label_temp.pack()

label_desc = ttk.Label(frame, text="", font=("Segoe UI", 11))
label_desc.pack()

label_wind = ttk.Label(frame, text="", font=("Segoe UI", 10))
label_wind.pack()

root.mainloop()
